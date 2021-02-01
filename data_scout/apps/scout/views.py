import json
import os

from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from pyparsing import ParseException
from rest_framework import viewsets, views, response, status
from rest_framework import permissions
from rest_framework.response import Response

import data_scout
import math
import numpy as np
from .serializers import DataSourceSerializer, RecipeSerializer, TransformationSerializer, FlowSerializer, \
    JoinSerializer, FlowStepSerializer, TransformationSerializerUpdate, RecipeFolderSerializer, \
    DataSourceFolderSerializer
from .models import DataSource, Recipe, Transformation, Flow, Join, FlowStep, RecipeFolder, DataSourceFolder
from django.core.exceptions import ObjectDoesNotExist


class DataSourceViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = DataSource.objects.all()
    serializer_class = DataSourceSerializer
    permission_classes = [permissions.IsAuthenticated]


class LoginCheckView(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        return response.Response({"success": True})


class DataSourceTypesView(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        data_source_types = data_scout.connectors.DataSourceType.data_source_types
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


class FlowViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Flow.objects.all()
    serializer_class = FlowSerializer
    permission_classes = [permissions.IsAuthenticated]


class JoinViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Join.objects.all()
    serializer_class = JoinSerializer
    permission_classes = [permissions.IsAuthenticated]


class FlowStepViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = FlowStep.objects.all()
    serializer_class = FlowStepSerializer
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


def data(request, recipe: int):
    """
    Load the data.
    TODO: Check if we want to reintroduce the "step" (i.e. to offer the option to get the dataset after a certain step
    in the recipe).
    :param request:
    :param recipe:
    :param step:
    :return:
    """
    recipe = get_object_or_404(Recipe, pk=recipe)
    messages = []
    success = True
    records_export, columns = [], []
    t = -1
    try:
        data_source = {"source": recipe.input.source, "kwargs": json.loads(recipe.input.kwargs)}
        if "filename" in data_source["kwargs"]:
            # In this case, we need to append the upload directory
            data_source["kwargs"]["filename"] = os.path.join(settings.MEDIA_ROOT, data_source["kwargs"]["filename"])
        pipeline = _get_pipeline(recipe)
        scout = data_scout.scout.Scout()
        executor = data_scout.executor.PandasExecutor(data_source, pipeline, scout)
        records, columns = executor(column_types=True)

        records_export = []
        clean_func = CleanJSON()
        for i, record in enumerate(records):
            records_export.append(list(clean_func(record, i)[0].values()))

        # TODO: Retrieve t on error
    except TypeError as e:
        success = False
        messages.append({"code": 2, "type": "error", "message": f"Transformation {t}: {e}"})
    except ParseException as e:
        success = False
        messages.append(
            {"code": -1, "type": "error", "message": f"Transformation {t}: There is an error in the equation. {e}"})
    except data_scout.exceptions.IndexFilterException as e:
        messages.append({"code": -1, "type": "warning", "message": f"Transformation {t}: {e}"})
    except data_scout.exceptions.TransformationUnavailableException as e:
        messages.append({"code": -1, "type": "warning", "message": f"Transformation {e.transformation}: {e}"})

    if not success:
        return JsonResponse({"success": False, "messages": messages})

    return JsonResponse({"success": True, "messages": messages, "data": {
        'records': records_export,
        "column_types": columns,
        "column_names": list(columns[-1].keys())
    }})


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



