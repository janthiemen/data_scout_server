import json

from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404

from django.contrib.auth.models import User, Group
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


def data(request, recipe: int, step: int):
    recipe = get_object_or_404(Recipe, pk=recipe)
    messages = []
    success = True
    # Load the data
    # TODO:
    csv = data_sources.CSV({"filename": "test.csv", "delimiter": ",", "has_header": True, "encoding": "utf-8"})
    df = csv(True, "random")
    try:
        transformation = recipe.transformations.filter(previous__isnull=True).get()
    except ObjectDoesNotExist as e:
        transformation = None

    def _is_false(value):
        return value != False

    # do ... while
    t = 1
    records = df.to_dict('records')
    while transformation is not None:
        # Execute the transformation on the data set
        try:
            if transformation.transformation not in TRANSFORMATION_MAP:
                messages.append({
                    "code": 3,
                    "message": "Transformation {}: The transformation {} doesn't exist".format(
                        t,
                        transformation.transformation
                    )
                })
            else:
                t_func = TRANSFORMATION_MAP[transformation.transformation](json.loads(transformation.kwargs))
                for i, record in enumerate(records):
                    records[i] = t_func(record)
                if t_func.filter:
                    records = filter(_is_false, records)
            transformation = transformation.next.get()
            t += 1
        except ObjectDoesNotExist:
            # When there's no next transformation we're done
            break
        except TypeError as e:
            success = False
            messages.append({"code": 2, "message": "Transformation {}: {}".format(t, str(e))})
            break

    if not success:
        return JsonResponse({"success": False, "messages": messages})

    records_export = []
    clean_func = CleanJSON()
    for record in records:
        records_export.append(list(clean_func(record).values()))

    return JsonResponse({"success": True, "data": {'records': records_export, "columns": list(records[0].keys())}})


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



