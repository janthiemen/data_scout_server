from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import DataSource, Recipe, Transformation, Flow, Join, FlowStep


class DataSourceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = DataSource
        fields = ['id', 'name', 'source', 'kwargs']


class RecipeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Recipe
        fields = ['id', 'name', 'input', 'output']


class TransformationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Transformation
        fields = ['id', 'recipe', 'transformation', 'kwargs']


class FlowSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Flow
        fields = ['id', 'name', 'sink']


class JoinSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Join
        fields = ['id', 'data_source_left', 'data_source_right', 'method', 'field_left', 'field_right', 'join_query']


class FlowStepSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = FlowStep
        fields = ['id', 'flow', 'recipe', 'join']
