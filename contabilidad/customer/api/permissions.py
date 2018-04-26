from rest_framework import permissions
from django.utils.translation import ugettext as _


class AdminAndCollaboratorPermission(permissions.BasePermission):

    message = _('You need to be an admin or company collaborator')

    def has_permission(self, request, view):
        user = request.user
        if user.is_authenticated:
            if request.method in permissions.SAFE_METHODS:
                return True
            if user.is_staff or user.is_superuser:
                return True
        return False

    def has_object_permission(self, request, view, obj):
        user = request.user
        if user.is_authenticated:
            if user.is_staff or user.is_superuser:
                return True
            if obj.collaborators.filter(pk=user.pk).exists():
                return True
        return False
