from rest_framework.permissions import BasePermission


class IsPlaceAuthorOrSu(BasePermission):
    def has_object_permission(self, request, view, place):
        if request.user is None:
            return False

        if request.user.is_superuser:
            return True

        if place.host == request.user:
            return True

        return False


class IsImageAuthorOrSu(BasePermission):
    def has_object_permission(self, request, view, image):
        if request.user is None:
            return False

        if request.user.is_superuser:
            return True

        if image.place.host == request.user:
            return True

        return False
