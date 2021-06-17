import json
import logging
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404

from rest_framework import viewsets, views, response, status
from rest_framework import permissions
from rest_framework.response import Response

import data_scout
import math
import numpy as np

from .datasources import _data_source_to_pipeline, _data_source_to_dict
from .iam import ProjectModelView
from .permissions import TransformationPermission
from ..serializers import RecipeSerializer, TransformationSerializer, TransformationSerializerUpdate, RecipeFolderSerializer
from ..models import Recipe, Transformation, RecipeFolder
from django.core.exceptions import ObjectDoesNotExist

from ..variable_logger import VariableLogger


class TransformationTypesView(views.APIView):
    """
    Get an overview of the available transformation types.
    """
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        """
        Get all transformation types.
        """
        scout = data_scout.scout.Scout()
        transformation_types = list(scout.transformations.values())
        serialized = []
        for transformation_type in transformation_types:
            serialized.append({"name": transformation_type.__name__, "fields": transformation_type.fields})

        return response.Response(serialized)


class RecipeViewSet(ProjectModelView):
    """
    API endpoint that allows users to be viewed or edited.
    Use ?orphans_only=1 to only select top level recipes
    """
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

    def get_queryset(self):
        """
        Get the queryset, depending on the "orphans_only" parameter. If this parameter is set to 1, only flows without
        a parent folder are returned.
        """
        orphans_only = self.request.query_params.get("orphans_only", 0) == 1
        queryset = self.queryset.filter(project=self.request.user.profile.project.project)
        if orphans_only:
            queryset = queryset.filter(parent=None)
        return queryset


class RecipeFolderViewSet(ProjectModelView):
    """
    API endpoint that allows users to be viewed or edited.
    Use ?orphans_only=1 to only select top level folders
    """
    queryset = RecipeFolder.objects.all()
    serializer_class = RecipeFolderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Get the queryset, depending on the "orphans_only" parameter. If this parameter is set to 1, only folders without
        a parent folder are returned.
        """
        orphans_only = int(self.request.query_params.get("orphans_only", 0)) == 1
        queryset = self.queryset.filter(project=self.request.user.profile.project.project)
        if orphans_only:
            queryset = queryset.filter(parent=None)
        return queryset


class TransformationViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows transformations to be viewed or edited.
    """
    permission_classes = [permissions.IsAuthenticated, TransformationPermission]
    queryset = Transformation.objects.all()
    serializer_class = TransformationSerializer

    def destroy(self, request, *args, **kwargs):
        """
        Delete a transformation. If this transformation is followed by another, it will take care of that before deletion.
        """
        transformation = self.get_object()
        try:
            transformation_next = transformation.next.get()
            transformation_next.previous = transformation.previous
            transformation_next.save()
        except ObjectDoesNotExist as e:
            pass
        transformation.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_serializer_class(self):
        """
        Get the serializer class. In order to update we need a different serializer that doesn't use the next related
        name.
        """

        serializer_class = self.serializer_class

        if self.request.method == 'PUT':
            serializer_class = TransformationSerializerUpdate

        return serializer_class


def _get_pipeline(recipe: Recipe):
    """
    Generate a JSON pipeline definition, based on a recipe object.

    :param recipe: The flow to transform to a JSON file
    :return:
    """
    try:
        transformation = recipe.transformations.filter(previous__isnull=True).get()
    except ObjectDoesNotExist as e:
        transformation = None

    pipeline = []
    while transformation is not None:
        # Execute the transformation on the data set
        try:
            pipeline.append({"transformation": transformation.transformation,
                             "kwargs": json.loads(transformation.kwargs)})
            transformation = transformation.next.get()
        except ObjectDoesNotExist:
            # When there's no next transformation we're done
            break
    return pipeline


class CleanJSON:
    """
    This transformation cleans to object to present valid JSON. It's NOT meant to be used by the user. This is only for
    internal usage.
    """
    def __call__(self, row, index: int):
        for key, value in row.items():
            if value is math.nan or (isinstance(value, float) and np.isnan(value)):
                row[key] = "NaN"

        return row, index


def _recipe_to_pipeline(recipe: Recipe, scout: data_scout.scout.Scout, use_sample=True, column_types=True):
    """
    Convert a Recipe object to a complete pipeline definition, including the data source.

    :param recipe: The recipe to convert
    :param scout: An initialized data scout Scout object
    :param use_sample: If True sample the dataset, if False use all data.
    :param column_types: If True return the column types as well (more overhead), if False then don't include them
    :return:
    """

    if recipe.input is not None:
        data_source = _data_source_to_dict(recipe.input, scout)
    elif recipe.input_join is not None:
        # If the input to this flow is a join, we need to construct it.
        if recipe.input_join.data_source_left is not None:
            data_source_left = _data_source_to_pipeline(recipe.input_join.data_source_left, scout, use_sample,
                                                        column_types)
        elif recipe.input_join.recipe_left is not None:
            data_source_left = _recipe_to_pipeline(recipe.input_join.recipe_left, scout, use_sample, column_types)
        else:
            raise ValueError("You need a data source OR a pipeline on the left")

        if recipe.input_join.data_source_right is not None:
            data_source_right = _data_source_to_pipeline(recipe.input_join.data_source_right, scout, use_sample,
                                                         column_types)
        elif recipe.input_join.recipe_right is not None:
            data_source_right = _recipe_to_pipeline(recipe.input_join.recipe_right, scout, use_sample, column_types)
        else:
            raise ValueError("You need a data source OR a pipeline on the right")

        data_source = {
            "source": "join",
            "kwargs": {
                "left": data_source_left,
                "right": data_source_right,
                "on_left": recipe.input_join.field_left.split(","),
                "on_right": recipe.input_join.field_right.split(","),
                "how": recipe.input_join.method
            }
        }
    else:
        raise ValueError("You need a data source to generate the pipeline")

    definition = {
        "use_sample": use_sample,
        "sampling_technique": recipe.sampling_technique,
        "column_types": column_types,
        "data_source": data_source,
        "pipeline": _get_pipeline(recipe)
    }
    return definition


def data(request, recipe: int):
    """
    Load the data and execute a pipeline.

    :param request:
    :param recipe: The id of the recipe
    :return:
    """
    logger = logging.getLogger(__name__)
    variable_logger = VariableLogger(1)
    logger.addHandler(variable_logger.log_handler)
    logger.setLevel(logging.INFO)

    success = True
    records_export, columns = [], []
    try:
        scout = data_scout.scout.Scout(logger=logger)
        recipe = get_object_or_404(Recipe, pk=recipe)
        definition = _recipe_to_pipeline(recipe, scout, use_sample=True, column_types=True)
        records, columns = scout.execute_json(definition, data_scout.executor.PandasExecutor)

        # After running the script, we store the new data schema
        recipe.schema = json.dumps(columns[-1])
        recipe.save()

        records_export = []
        clean_func = CleanJSON()
        for i, record in enumerate(records):
            records_export.append(list(clean_func(record, i)[0].values()))

    except data_scout.exceptions.PipelineException as e:
        success = False
        logger.error(f"Transformation: {e.transformation}: {type(e.original_exception).__name__} {e.original_exception}")

    if not success:
        return JsonResponse({"success": False, "messages": variable_logger.contents()})

    return JsonResponse({"success": True, "messages": variable_logger.contents(), "data": {
        'records': records_export,
        "column_types": columns,
        "column_names": list(columns[-1].keys())
    }})


def pipeline(request, recipe: int):
    """
    Export a complete pipeline as either Python code or as a JSON definition, depending on the "output" get parameter.

    :param request:
    :param recipe:
    :return:
    """
    scout = data_scout.scout.Scout()
    recipe = get_object_or_404(Recipe, pk=recipe)
    definition = _recipe_to_pipeline(recipe, scout)
    if request.GET.get("output") == "python":
        scout = data_scout.scout.Scout()
        code, _ = scout.execute_json(definition, data_scout.executor.CodeExecutor)
        res = HttpResponse(code, content_type='text/x-python')
        res['Content-Disposition'] = 'attachment; filename="pipeline.py"'
        return res
    else:
        return JsonResponse(definition)


def meta_transformations(request):
    """
    Request a list of all transformations.

    :param request:
    :return:
    """
    scout = data_scout.scout.Scout()
    return JsonResponse({
        key: {"title": transformation.title, "key": transformation.key, "fields": transformation.fields}
        for key, transformation in scout.transformations.items()}
    )
