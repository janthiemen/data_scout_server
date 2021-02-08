import json
import logging
import mimetypes
import os
import uuid
from wsgiref.util import FileWrapper

from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404

from pyparsing import ParseException
from rest_framework import viewsets, views, response, status
from rest_framework import permissions
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response

import data_scout
import math
import numpy as np
from .serializers import DataSourceSerializer, RecipeSerializer, TransformationSerializer, \
    JoinSerializer, TransformationSerializerUpdate, RecipeFolderSerializer, \
    DataSourceFolderSerializer, UserFileSerializer
from .models import DataSource, Recipe, Transformation, Join, RecipeFolder, DataSourceFolder, UserFile
from django.core.exceptions import ObjectDoesNotExist

from .variable_logger import VariableLogger


def _is_int(val):
    try:
        int(val)
        return True
    except:
        return False


class DataSourceViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = DataSource.objects.all()
    serializer_class = DataSourceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def _make_schema(self, request):
        # We try if the data source actually works and what the data schema looks like
        definition = {"use_sample": True,
                      "sampling_technique": "top",
                      "column_types": True}
        data_source = {"source": request.data["source"], "kwargs": json.loads(request.data["kwargs"])}

        scout = data_scout.scout.Scout()
        ds = scout.get_data_source(data_source["source"])
        # Sometimes a data source is created that isn't ready to be tested (e.g. because the files still need to be
        # uploaded.
        ready = True
        for field_name, field in ds.fields.items():
            if field["type"] == "file":
                if field_name in data_source["kwargs"] and _is_int(data_source["kwargs"][field_name]):
                    user_file = UserFile.objects.get(pk=data_source["kwargs"][field_name])
                    data_source["kwargs"][field_name] = os.path.join(settings.MEDIA_ROOT, user_file.file_name)
                else:
                    ready = False
        if ready:
            definition["data_source"] = data_source
            definition["pipeline"] = []
            records, columns = scout.execute_json(definition, data_scout.executor.PandasExecutor)
            request.data["schema"] = json.dumps(columns[-1])
        return request

    def update(self, request, *args, **kwargs):
        request = self._make_schema(request)
        return super().update(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        request = self._make_schema(request)
        return super().create(request, *args, **kwargs)


class UserFileViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = UserFile.objects.all()
    serializer_class = UserFileSerializer
    # permission_classes = [permissions.IsAuthenticated]

    def get(self, user_file: int):
        return JsonResponse({"user_file": user_file})

    def retrieve(self, request, pk=None, **kwargs):
        user_file = get_object_or_404(self.queryset, pk=pk)
        if request.query_params.get("output", "json") == "file":
            with default_storage.open(user_file.file_name) as f:
                res = HttpResponse(FileWrapper(f), content_type=mimetypes.guess_type(user_file.original_file_name))
                res['Content-Disposition'] = f"attachment; filename={user_file.original_file_name}"
                return res
        else:
            serializer = self.serializer_class(user_file)
            return Response(serializer.data)
    # TODO: Add some sort of on delete to delete the accompanying file


class UserFileUploadView(views.APIView):
    parser_classes = [FileUploadParser]
    queryset = UserFile.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, user_file_id: int, format=None):
        file_name = str(uuid.uuid4())
        user_file = get_object_or_404(UserFile, pk=user_file_id)

        # If there's already a file, we'll delete it
        if user_file.file_name is not None and default_storage.exists(user_file.file_name):
            default_storage.delete(user_file.file_name)

        file_obj = request.data['file']
        default_storage.save(file_name, ContentFile(file_obj.read()))
        user_file.file_name = file_name
        user_file.original_file_name = request.data['file'].name
        user_file.save()

        serializer = UserFileSerializer(user_file, many=False)
        return Response(serializer.data)


class LoginCheckView(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        return response.Response({"success": True})


class DataSourceTypesView(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        scout = data_scout.scout.Scout()
        data_source_types = scout.data_sources
        serialized = []
        for data_source_type in data_source_types.values():
            serialized.append({"name": data_source_type.__name__, "fields": data_source_type.fields})

        # content = {'message': 'Hello, World!'}
        return response.Response(serialized)


class TransformationTypesView(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        scout = data_scout.scout.Scout()
        transformation_types = list(scout.transformations.values())
        serialized = []
        for transformation_type in transformation_types:
            serialized.append({"name": transformation_type.__name__, "fields": transformation_type.fields})

        return response.Response(serialized)


class RecipeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    Use ?orphans_only=1 to only select top level recipes
    """
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        orphans_only = self.request.query_params.get("orphans_only", 0) == 1
        queryset = self.queryset
        if orphans_only:
            queryset = queryset.filter(parent=None)
        return queryset


class RecipeFolderViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    Use ?orphans_only=1 to only select top level folders
    """
    queryset = RecipeFolder.objects.all()
    serializer_class = RecipeFolderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        orphans_only = int(self.request.query_params.get("orphans_only", 0)) == 1
        queryset = self.queryset
        if orphans_only:
            queryset = queryset.filter(parent=None)
        return queryset


class DataSourceFolderViewSet(RecipeFolderViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    Use ?orphans_only=1 to only select top level folders
    """
    queryset = DataSourceFolder.objects.all()
    serializer_class = DataSourceFolderSerializer
    permission_classes = [permissions.IsAuthenticated]


class TransformationViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Transformation.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TransformationSerializer

    def destroy(self, request, *args, **kwargs):
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


class JoinViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Join.objects.all()
    serializer_class = JoinSerializer
    permission_classes = [permissions.IsAuthenticated]


def _get_pipeline(recipe):
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


def _data_source_to_dict(data_source: DataSource, scout: data_scout.scout.Scout):
    data_source = {"source": data_source.source, "kwargs": json.loads(data_source.kwargs)}
    ds = scout.get_data_source(data_source["source"])
    for field_name, field in ds.fields.items():
        if field["type"] == "file":
            user_file = UserFile.objects.get(pk=data_source["kwargs"][field_name])
            data_source["kwargs"][field_name] = os.path.join(settings.MEDIA_ROOT, user_file.file_name)
    return data_source


def _data_source_to_pipeline(data_source: DataSource, scout: data_scout.scout.Scout, use_sample=True, column_types=True,
                             sampling_technique: str = 'top'):
    # data_source = get_object_or_404(DataSource, pk=data_source)
    return {
        "use_sample": use_sample,
        "sampling_technique": sampling_technique,
        "column_types": column_types,
        "data_source": _data_source_to_dict(data_source, scout),
        "pipeline": []
    }


def _recipe_to_pipeline(recipe: Recipe, scout: data_scout.scout.Scout, use_sample=True, column_types=True):
    if recipe.input is not None:
        data_source = _data_source_to_dict(recipe.input, scout)
    elif recipe.input_join is not None:
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
    :param recipe:
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


# Create your views here.
def recipe_get_recipe():
    pass


def flows_get_flows():
    pass


def flows_get_flow():
    pass


def flows_post_flows():
    pass

"""

Screens:
- Flows overview
    - Flows overview
        flows_get_flows()
    - Add flow button
        flows_post_flow()
    - Edit flow
        flows_post_flow()
    
- Data sources overview
    - Data sources overview
        data_sources_get_data_sources()
    - Add data source button
        data_sources_post_data_source()
            
- Flow edit
    - Line drawer
    - Add step(/recipe)
    - Go to step(/recipe)
    
- Recipe edit
    - Spreadsheet like page
    - Add recipe steps
    - Get preview
"""



