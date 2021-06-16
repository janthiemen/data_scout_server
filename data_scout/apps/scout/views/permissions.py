from rest_framework import permissions
from django.core.exceptions import FieldDoesNotExist


class ProjectPermission(permissions.BasePermission):
    """
    Object-level permission to only allow member of the respective projects to read or edit an object.
    """

    def has_object_permission(self, request, view, obj):
        try:
            obj._meta.get_field("project")
            users = obj.project.users.all()
        except FieldDoesNotExist:
            # The "Project" object itself doesn't have a project field
            users = obj.users.all()
        user_permissions = [up
                            for up in users
                            if up.user == request.user and (request.method in permissions.SAFE_METHODS or
                                                            up.role in ('owner', 'admin', 'editor'))]

        if len(user_permissions) == 0 and not request.user.is_staff:
            return False
        else:
            return True


class UserProfilePermission(permissions.BasePermission):
    """
    Object-level permission to only allow the owner of the profile to view and edit it.
    """

    def has_object_permission(self, request, view, obj):
        if obj.user == request.user:
            return True
        else:
            return False

