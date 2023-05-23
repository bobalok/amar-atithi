from rest_framework.permissions import BasePermission


class IsSuperUser(BasePermission):

    def has_permission(self, request, view):
        if request.user is not None and request.user.is_superuser:
            return True

        return False


