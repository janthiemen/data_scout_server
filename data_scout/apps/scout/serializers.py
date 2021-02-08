from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import DataSource, Recipe, Transformation, Join, RecipeFolder, DataSourceFolder, UserFile


class DataSourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataSource
        fields = ['id', 'name', 'parent', 'source', 'kwargs', 'schema']


class UserFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFile
        fields = ['id', 'data_source', 'field_name', 'file_name', 'original_file_name']


class TransformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transformation
        fields = ['id', 'recipe', 'transformation', 'previous', 'next', 'kwargs']


class TransformationSerializerUpdate(serializers.ModelSerializer):
    class Meta:
        model = Transformation
        fields = ['id', 'recipe', 'transformation', 'previous', 'kwargs']


class RecipeSerializer(serializers.ModelSerializer):
    transformations = TransformationSerializer(many=True, read_only=True)

    # TODO: Add the option to return a more limited set
    class Meta:
        model = Recipe
        fields = ['id', 'name', 'input', 'input_join', 'output', 'transformations', 'parent', 'schema']


class RecursiveField(serializers.Serializer):
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class RecipeFolderSerializer(serializers.ModelSerializer):
    child_folders = RecursiveField(many=True, read_only=True)
    children = RecipeSerializer(many=True, read_only=True)

    class Meta:
        model = RecipeFolder
        fields = ['id', 'name', 'parent', 'child_folders', 'children']


class DataSourceFolderSerializer(serializers.ModelSerializer):
    child_folders = RecursiveField(many=True, read_only=True)
    children = DataSourceSerializer(many=True, read_only=True)

    class Meta:
        model = DataSourceFolder
        fields = ['id', 'name', 'parent', 'child_folders', 'children']


class JoinSerializer(serializers.ModelSerializer):
    data_source_left = DataSourceSerializer(many=False, read_only=True)
    data_source_right = DataSourceSerializer(many=False, read_only=True)
    recipe_left = RecipeSerializer(many=False, read_only=True)
    recipe_right = RecipeSerializer(many=False, read_only=True)

    class Meta:
        model = Join
        fields = ['id', 'name', 'data_source_left', 'recipe_left', 'data_source_right', 'recipe_right', 'method',
                  'field_left', 'field_right']
