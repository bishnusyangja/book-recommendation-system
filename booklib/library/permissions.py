from rest_framework.permissions import BasePermission


class AdminWritePermission(BasePermission):
    """
    Custom permission to only allow certain HTTP methods.
    """
    def has_permission(self, request, view):
        if request.method.lower() in ('get', 'option'):
            return True
        else:
            # is_staff refers to the admin staff
            if request.user.is_staff:
                return True
        return False
