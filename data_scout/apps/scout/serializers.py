from django.contrib.auth.models import User
from rest_framework import serializers
from .models import DataSource, Recipe, Transformation, Join, RecipeFolder, DataSourceFolder, UserFile, UserProject, \
    Project, UserProfile


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'name']


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username']


class UserProjectFullSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False, read_only=True)

    class Meta:
        model = UserProject
        fields = ['id', 'user', 'role']


class UserProjectSerializer(serializers.ModelSerializer):
    project = ProjectSerializer(many=False, read_only=True)

    class Meta:
        model = UserProject
        fields = ['id', 'project', 'user', 'role']


class UserProjectCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProject
        fields = ['id', 'project', 'user', 'role']


class ProjectFullSerializer(serializers.ModelSerializer):
    users = UserProjectFullSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = ['id', 'name', 'users']


class UserProfileSerializer(serializers.ModelSerializer):
    project = UserProjectSerializer(many=False, read_only=True)

    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'project']


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    # project = UserProjectSerializer(many=False, read_only=False)
    project = serializers.PrimaryKeyRelatedField(queryset=UserProject.objects.all(), read_only=False)

    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'project']


class DataSourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataSource
        fields = ['id', 'name', 'parent', 'source', 'kwargs', 'schema', 'project']


class UserFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFile
        fields = ['id', 'data_source', 'field_name', 'file_name', 'original_file_name', 'project']


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
        fields = ['id', 'name', 'input', 'input_join', 'output', 'transformations', 'parent', 'schema', 'project']


class RecursiveField(serializers.Serializer):
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class RecipeFolderSerializer(serializers.ModelSerializer):
    child_folders = RecursiveField(many=True, read_only=True)
    children = RecipeSerializer(many=True, read_only=True)

    class Meta:
        model = RecipeFolder
        fields = ['id', 'name', 'parent', 'child_folders', 'children', 'project']


class JoinSerializer(serializers.ModelSerializer):
    data_source_left = DataSourceSerializer(many=False, read_only=True)
    data_source_right = DataSourceSerializer(many=False, read_only=True)
    recipe_left = RecipeSerializer(many=False, read_only=True)
    recipe_right = RecipeSerializer(many=False, read_only=True)

    class Meta:
        model = Join
        fields = ['id', 'name', 'data_source_left', 'recipe_left', 'data_source_right', 'recipe_right', 'method',
                  'field_left', 'field_right', 'parent', 'project']


class DataSourceFolderSerializer(serializers.ModelSerializer):
    child_folders = RecursiveField(many=True, read_only=True)
    children = DataSourceSerializer(many=True, read_only=True)
    child_joins = JoinSerializer(many=True, read_only=True)

    class Meta:
        model = DataSourceFolder
        fields = ['id', 'name', 'parent', 'child_folders', 'children', 'child_joins', 'project']


