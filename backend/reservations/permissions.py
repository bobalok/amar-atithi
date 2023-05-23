from rest_framework.permissions import BasePermission

class IsReservationAuthorOrSu(BasePermission):
    def has_object_permission(self, request, view, reservation):
        if request.user is None:
            return False

        if reservation.guest == request.user or request.user.is_superuser:
            return True

        return False

class IsReservationPlaceAuthor(BasePermission):
    def has_object_permission(self, request, view, reservation):
        if request.user is None:
            return False

        if reservation.place.host == request.user or request.user.is_superuser:
            return True

        return False


class CanViewReservation(BasePermission):
    def has_object_permission(self, request, view, reservation):
        if request.user is None:
            return False

        if reservation.place.host == request.user or reservation.guest == request.user or request.user.is_superuser:
            return True

        return False

class NotReservationPlaceAuthor(BasePermission):
    def has_object_permission(self, request, view, reservation):
        if reservation.place.host != request.user:
            return True

        return False
