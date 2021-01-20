import json
from typing import List

from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404

from django.contrib.auth.models import User, Group
from pyparsing import ParseException
from rest_framework import viewsets, views, response, status
from rest_framework import permissions, authentication
from rest_framework.response import Response

from apps.scout import transformations
from apps.scout.transformations import TRANSFORMATION_MAP
from apps.scout.transformations.data import CleanJSON
from .serializers import DataSourceSerializer, RecipeSerializer, TransformationSerializer, FlowSerializer, \
    JoinSerializer, FlowStepSerializer, TransformationSerializerUpdate
from .models import DataSource, Recipe, Transformation, Flow, Join, FlowStep
from . import data_sources
from django.core.exceptions import ObjectDoesNotExist

from .transformations import _utils
from .transformations.filter import IndexFilterException

import pandas as pd

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
        data_source_types = [data_sources.BigQuery, data_sources.CSV]
        serialized = []
        for data_source_type in data_source_types:
            serialized.append({"name": data_source_type.__name__, "fields": data_source_type.fields})

        # content = {'message': 'Hello, World!'}
        return response.Response(serialized)


class TransformationTypesView(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        transformation_types = list(transformations.TRANSFORMATION_MAP.values())
        serialized = []
        for transformation_type in transformation_types:
            serialized.append({"name": transformation_type.__name__, "fields": transformation_type.fields})

        return response.Response(serialized)


class RecipeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
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


def _get_transformations(recipe, messages):
    try:
        transformation = recipe.transformations.filter(previous__isnull=True).get()
    except ObjectDoesNotExist as e:
        transformation = None

    t = 1
    transformation_list = []
    while transformation is not None:
        # Execute the transformation on the data set
        try:
            if transformation.transformation not in TRANSFORMATION_MAP:
                messages.append({
                    "code": 3,
                    "type": "warning",
                    "message": "Transformation {}: The transformation {} doesn't exist".format(
                        t,
                        transformation.transformation
                    )
                })
            else:
                transformation_list.append((t, transformation, TRANSFORMATION_MAP[transformation.transformation]))
                transformation = transformation.next.get()
                t += 1
        except ObjectDoesNotExist:
            # When there's no next transformation we're done
            break
    return transformation_list, messages


def _get_sampling_technique(recipe, transformation_list, messages):
    # Not every transformation can be used with all sampling techniques. We'll determine which is allowed.
    allowed_sampling_techniques = [transformation.allowed_sampling_techniques
                                   for _, _, transformation in transformation_list]
    result = set(allowed_sampling_techniques[0]).intersection(*allowed_sampling_techniques[1:])
    if recipe.sampling_technique in result:
        return recipe.sampling_technique, messages
    elif len(result) == 0:
        messages.append({
            "code": -1,
            "type": "warning",
            "message": f"Couldn't find a sampling technique that satisfies all requirements. Using {recipe.sampling_technique}, expect unexpected behaviour."})
        return recipe.sampling_technique, messages
    else:
        for key, _ in Recipe.SAMPLING_TECHNIQUE_CHOICES:
            if key in result:
                messages.append({
                    "code": -1,
                    "type": "info",
                    "message": f"Switched from sampling technique {recipe.sampling_technique} to {key} because of requirements by the transformations."})
                return key, messages


def data(request, recipe: int, step: int):
    recipe = get_object_or_404(Recipe, pk=recipe)
    messages = []
    transformation_list, messages = _get_transformations(recipe, messages)
    sampling_technique, messages = _get_sampling_technique(recipe, transformation_list, messages)

    success = True
    # Load the data
    # TODO: Get this from the database
    csv = data_sources.CSV({"filename": "test.csv", "delimiter": ",", "has_header": True, "encoding": "utf-8"})
    df = csv(True, sampling_technique)

    def _is_false(value):
        return value != False

    records = df.to_dict('records')
    columns = []
    sample_size = len(records)
    for t, transformation, t_class in transformation_list:
        # Execute the transformation on the data set
        try:
            # Before each transformation we create a list of columns and column types that are available at that point
            columns.append(_utils.get_columns(records))
            t_func = t_class(json.loads(transformation.kwargs), sample_size, records[0])
            # If it's a global transformation, we'll call it on all records, if it isn't, we call it one-at-a-time
            # TODO: Check if we could do all of this in a DF apply?
            if t_func.is_global:
                records, _ = t_func(records, -1)
            else:
                for i, record in enumerate(records):
                    records[i], _ = t_func(record, i)
            if t_func.filter:
                records = [record for record in filter(_is_false, records)]
                # TODO: Make sure we're still returning records, even if an error occurs
        except TypeError as e:
            success = False
            messages.append({"code": 2, "type": "error", "message": f"Transformation {t}: {e}"})
            break
        except ParseException as e:
            success = False
            messages.append({"code": -1, "type": "error", "message": f"Transformation {t}: There is an error in the equation. {e}"})
            break
        except IndexFilterException as e:
            messages.append({"code": -1, "type": "warning", "message": f"Transformation {t}: {e}"})
            break
        # except Exception as e:
        #     success = False
        #     messages.append({"code": -1, "type": "error", "message": f"Transformation {t}: {e}"})
        #     break

    if not success:
        return JsonResponse({"success": False, "messages": messages})

    records_export = []
    clean_func = CleanJSON()
    records_df = pd.DataFrame(records).to_dict(orient="records")
    # column_types = [type(val).__name__ for key, val in records_df[0].items()]
    columns.append(_utils.get_columns(records))
    for i, record in enumerate(records_df):
        records_export.append(list(clean_func(record, i)[0].values()))

    return JsonResponse({"success": True, "messages": messages, "data": {
        'records': records_export,
        "columns": columns
    }})


def meta_transformations(request):
    """
    Request a list of all transformations.

    :param request:
    :return:
    """
    return JsonResponse({
        key: {"title": transformation.title, "fields": transformation.fields}
        for key, transformation in TRANSFORMATION_MAP.items()}
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



