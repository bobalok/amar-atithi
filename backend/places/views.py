from django.db.models import Q
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateAPIView, DestroyAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from places.components.serializers import UploadImageSerializer, ImageSerializer
from places.models import Place, City, Space, Image, Review
from places.permissions import IsPlaceAuthorOrSu, IsImageAuthorOrSu
from places.serializers import CreatePlaceSerializer, PlaceListSerializer, PlaceUpdateSerializer, PlaceDetailSerializer
from reservations.models import Calendar
from src.lib import rand_str
from users.models import User


class CreatePlaceView(CreateAPIView):
    serializer_class = CreatePlaceSerializer
    queryset = Place.objects.all()
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        city = serializer.validated_data['city']
        space = serializer.validated_data['space']
        title = "{} in {}".format(space.name, city.name)
        return serializer.save(title=title, host=self.request.user)


class PlaceListView(ListAPIView):
    serializer_class = PlaceListSerializer
    permission_classes = []

    def get_queryset(self):
        return Place.objects.filter(Q(host=self.request.user) & Q(deleted=False))


class PlaceSearchView(APIView):
    serializer_class = PlaceListSerializer
    permission_classes = []
    queryset = Place.objects.all()

    def post(self, request, *args, **kwargs):
        keyword = request.data.get("search", "")
        guest = request.data.get("guest", 1)
        min = request.data.get("min")
        max = request.data.get("max")
        checkin = request.data.get("checkin")
        checkout = request.data.get("checkout")
        place_type = request.data.get("type")
        spaces = request.data.get("spaces")

        query = Place.objects.filter(Q(title__icontains=keyword) | Q(city__name__icontains=keyword))

        if guest:
            query = query.filter(Q(max_guest__gte=guest))

        if min:
            query = query.filter(Q(price__gte=min))

        if max:
            query = query.filter(Q(price__lte=max))

        print(spaces)
        print(type(spaces))
        print(100)

        if place_type:
            query = query.filter(Q(type_id__in=place_type))

        if spaces:
            query = query.filter(Q(space_id__in=spaces))

        if checkin and checkout:
            exQuery = Calendar.objects.filter(Q(date__range=[checkin, checkout])).values_list("place",
                                                                                              flat=True).distinct()
            query = query.exclude(Q(id__in=exQuery))
        elif checkin:
            exQuery = Calendar.objects.filter(Q(date=checkin)).values_list("place", flat=True).distinct()
            query = query.exclude(Q(id__in=exQuery))
        elif checkout:
            exQuery = Calendar.objects.filter(Q(date=checkout)).values_list("place", flat=True).distinct()
            query = query.exclude(Q(id__in=exQuery))

        return Response(PlaceListSerializer(query, many=True, context=self.get_renderer_context()).data)


    # def post(self, request):
    #     query = request.data.get("query")
    #
    #     query = Place.objects.filter(
    #         Q(host__is_active=True) & Q(deleted=False)
    #     )
    #
    #     return Response(PlaceListSerializer(query, many=True).data)


class PlaceUpdateView(RetrieveUpdateAPIView):
    serializer_class = PlaceUpdateSerializer
    permission_classes = [IsAuthenticated, IsPlaceAuthorOrSu]
    queryset = Place.objects.filter(deleted=False)
    lookup_field = 'code'
    lookup_url_kwarg = 'code'

    def perform_update(self, serializer):
        return serializer.save(published=True)


class PlaceDetailView(RetrieveAPIView):
    serializer_class = PlaceDetailSerializer
    permission_classes = []
    queryset = Place.objects.filter(deleted=False, published=True)
    lookup_field = 'code'
    lookup_url_kwarg = 'code'


class SimilarPlaceView(ListAPIView):
    serializer_class = PlaceListSerializer
    permission_classes = []

    def get_queryset(self):
        code = self.kwargs.get("code")
        place = Place.objects.filter(code=code)

        if place.exists():
            return Place.objects.filter(
                Q(deleted=False) & Q(published=True) & (Q(city=place.first().city))
            ).exclude(code=code)[:8]
        else:
            return place


class UserListings(ListAPIView):
    serializer_class = PlaceListSerializer
    permission_classes = []

    def get_queryset(self):
        return Place.objects.filter(
            Q(deleted=False) & Q(published=True) & Q(host__userid=self.kwargs.get("userid"))
        )


class UploadImageView(CreateAPIView):
    serializer_class = UploadImageSerializer
    permission_classes = [IsAuthenticated, IsPlaceAuthorOrSu]
    queryset = Image.objects.all()


class DeleteImageView(DestroyAPIView):
    serializer_class = ImageSerializer
    permission_classes = [IsAuthenticated, IsImageAuthorOrSu]
    queryset = Image.objects.all()


class RecentlyAddedPlaces(ListAPIView):
    serializer_class = PlaceListSerializer
    permission_classes = []

    def get_queryset(self):
        return Place.objects.filter(Q(host__is_active=True) & Q(deleted=False) & Q(published=True)) \
                   .order_by("-created_at")[:8]
