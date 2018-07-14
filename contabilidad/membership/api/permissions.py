from rest_framework import permissions


class MembershipUpdatePermission(permissions.BasePermission):

    def has_permission(self, request, view, *args, **kwargs):

        is_logged = request.user.is_authenticated()
        is_admin = request.user.is_staff if is_logged else False

        print("is_logged: {}".format(is_logged))
        print("is_admin: {}".format(is_admin))
        print("view.action: {}".format(view.action))
        print("request.method: {}".format(request.method))

        if view.action == 'attachments' and is_logged and request.method in ['GET', 'POST']:
            return True

        if view.action == 'mine' and is_logged and request.method in ['GET', 'PATCH']:
            return True

        return True if is_logged and is_admin else False
