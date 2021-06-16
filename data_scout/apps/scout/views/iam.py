import json
import logging
import mimetypes
import os
import uuid
from wsgiref.util import FileWrapper

from django.conf import settings
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404

from rest_framework import viewsets, views, response, status, generics
from rest_framework import permissions
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response

import data_scout
import math
import numpy as np

from ..views.permissions import ProjectPermission, UserProfilePermission
from ..serializers import DataSourceSerializer, RecipeSerializer, TransformationSerializer, \
    JoinSerializer, TransformationSerializerUpdate, RecipeFolderSerializer, \
    DataSourceFolderSerializer, UserFileSerializer, UserProjectSerializer, UserProfileSerializer, ProjectSerializer, \
    UserProjectCreateSerializer, UserProfileUpdateSerializer, ProjectFullSerializer, UserSerializer, \
    ChangePasswordSerializer, UserDetailSerializer, CreateUserSerializer
from ..models import DataSource, Recipe, Transformation, Join, RecipeFolder, DataSourceFolder, UserFile, UserProject, \
    UserProfile, Project
from django.core.exceptions import ObjectDoesNotExist, FieldDoesNotExist

from ..variable_logger import VariableLogger


class ProjectModelView(viewsets.ModelViewSet):
    """
    Base viewset for project related resources. This should be extended by those viewsets.
    """
    permission_classes = [permissions.IsAuthenticated, ProjectPermission]

    def list(self, request, *args, **kwargs):
        """
        List the projects this user has access to.

        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        queryset = self.filter_queryset(self.get_queryset())

        for obj in queryset:
            self.check_object_permissions(request, obj)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        """
        Create a project.

        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        request.data["project"] = request.user.profile.project_id
        return super(ProjectModelView, self).create(request)

    def update(self, request, *args, **kwargs):
        """
        Update a project.

        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        request.data["project"] = request.user.profile.project_id
        return super(ProjectModelView, self).update(request)

    def get_queryset(self):
        """
        Get a pre-filtered queryset.

        :return:
        """
        queryset = self.queryset.filter(project=self.request.user.profile.project.project)
        return queryset


class LoginCheckView(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        return response.Response({"success": True})


class UserDetailView(views.APIView):
    serializer_class = UserDetailSerializer
    model = User
    permission_classes = (permissions.IsAuthenticated, )

    def get(self, request):
        serializer = self.serializer_class(request.user, many=False)
        return Response(serializer.data)

    def post(self, request):
        serializer = CreateUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Every user needs at least one project and a profile
        project = Project(name="Getting Started")
        project.save()
        user_project = UserProject(user=user, project=project)
        user_project.save()
        up = UserProfile(user=user, project=user_project)
        up.save()

        return Response(self.serializer_class(user, many=False).data)


class ChangePasswordView(generics.UpdateAPIView):
    """
    An endpoint for changing password. TODO: Should this be part of the user details?
    """
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (permissions.IsAuthenticated, permissions.IsAdminUser, )

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)


class UserProfileViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, UserProfilePermission]
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == "partial_update":
            return UserProfileUpdateSerializer
        else:
            return self.serializer_class


class ProjectViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, ProjectPermission]

    queryset = Project.objects.all()
    serializer_class = ProjectFullSerializer

    # TODO: Add some kind of security here
    # def get_queryset(self):
    #     return self.queryset.filter(user=self.request.user)


class UserProjectViewSet(ProjectModelView):
    queryset = UserProject.objects.all()
    serializer_class = UserProjectSerializer

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = UserProjectCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        serializer = self.get_serializer(self.get_queryset().get(pk=serializer.data.get("id")))

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
