from django.http import JsonResponse
from rest_framework.exceptions import ValidationError
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.utils import json
from rest_framework.views import APIView

from places.components.constants import checkin_times, checkout_times
from places.components.serializers import TypeDetailSerializer, TypeSerializer, SpaceSerializer, SpaceDetailSerializer, \
    CitySerializer, AmenitySerializer, RuleSerializer, ReviewCreateSerializer
from places.models import Type, Space, City, Amenity, Rule, Review, Place
from reservations.models import Reservation


class TypeList(ListAPIView):
    serializer_class = TypeSerializer
    queryset = Type.objects.filter(deleted=False)
    permission_classes = []


class SpaceList(ListAPIView):
    serializer_class = SpaceDetailSerializer
    queryset = Space.objects.all()
    permission_classes = []


class CityList(ListAPIView):
    serializer_class = CitySerializer
    queryset = City.objects.all()
    permission_classes = []


class AmenityList(ListAPIView):
    serializer_class = AmenitySerializer
    queryset = Amenity.objects.all()
    permission_classes = []


class RulesList(ListAPIView):
    serializer_class = RuleSerializer
    queryset = Rule.objects.all()
    permission_classes = []


class CheckInOutTimes(APIView):
    def get(self, request, *args, **kwargs):
        data = {
            'in': checkin_times(),
            'out': checkout_times()
        }

        return JsonResponse(data, safe=False)


class ReviewAGuestView(CreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewCreateSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        reservation = Reservation.objects.get(reference=request.data.get("reservation"))
        query = Review.objects.filter(reservation=reservation, type=1)

        if query.exists():
            raise ValidationError("You have already published your review")

        review = Review()
        review.review = request.data.get("review")
        review.rating = request.data.get("rating")
        review.reservation = reservation
        review.user = request.user
        review.type = 1
        review.save()

        invoice = reservation.invoice
        receiveable = invoice.receiveable
        host = reservation.place.host
        host.credit = host.credit + receiveable
        host.save()



        reservation.place.reviews.add(review)

        return Response(ReviewCreateSerializer(review).data)

class ReviewTripView(CreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewCreateSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        reservation = Reservation.objects.get(reference=request.data.get("reservation"))
        query = Review.objects.filter(reservation=reservation, type=0)

        if query.exists():
            raise ValidationError("You have already published your review")

        review = Review()
        review.review = request.data.get("review")
        review.rating = request.data.get("rating")
        review.reservation = reservation
        review.user = request.user
        review.type = 0
        review.save()

        reservation.place.reviews.add(review)

        return Response(ReviewCreateSerializer(review).data)