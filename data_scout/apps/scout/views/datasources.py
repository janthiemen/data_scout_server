import json
import mimetypes
import os
import uuid
from wsgiref.util import FileWrapper

from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404

from rest_framework import views, response
from rest_framework import permissions
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response

import data_scout

from ..views.iam import ProjectModelView
from ..serializers import DataSourceSerializer, UserFileSerializer, DataSourceFolderSerializer, JoinSerializer
from ..models import DataSource, UserFile, DataSourceFolder, Join


class DataSourceViewSet(ProjectModelView):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = DataSource.objects.all()
    serializer_class = DataSourceSerializer

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


class UserFileViewSet(ProjectModelView):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = UserFile.objects.all()
    serializer_class = UserFileSerializer

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

    def get_queryset(self):
        queryset = self.queryset.filter(project=self.request.user.profile.project.project)
        return queryset


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


class DataSourceTypesView(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        scout = data_scout.scout.Scout()
        data_source_types = scout.data_sources
        serialized = []
        for data_source_type in data_source_types.values():
            serialized.append({"name": data_source_type.__name__, "fields": data_source_type.fields})

        return response.Response(serialized)


class DataSourceFolderViewSet(ProjectModelView):
    """
    API endpoint that allows users to be viewed or edited.
    Use ?orphans_only=1 to only select top level folders
    """
    queryset = DataSourceFolder.objects.all()
    serializer_class = DataSourceFolderSerializer


class JoinViewSet(ProjectModelView):
    queryset = Join.objects.all()
    serializer_class = JoinSerializer


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



