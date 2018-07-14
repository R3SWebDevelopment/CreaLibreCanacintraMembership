from rest_framework import permissions


class MembershipUpdatePermission(permissions.BasePermission):

    def has_permission(self, request, view, *args, **kwargs):

        is_logged = request.user.is_authenticated()
        is_admin = request.user.is_staff if is_logged else False

        if view.action == 'attachments' and is_logged and request.method in ['GET', 'POST']:
            return True

        if view.action == 'mine' and is_logged and request.method in ['GET', 'PATCH']:
            return True

        is_valid_action = view.action not in ['partial_update', 'retrieve']
        is_valid_method = request.method in ['GET']

        return True if is_logged and is_admin and is_valid_action and is_valid_method else False
