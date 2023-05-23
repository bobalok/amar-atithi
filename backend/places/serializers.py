from rest_framework.fields import SerializerMethodField
from rest_framework.relations import SlugRelatedField
from rest_framework.serializers import ModelSerializer

from places.components.serializers import SpaceSerializer, ImageSerializer, TypeSerializer, CitySerializer, \
    AmenityViewSerializer, RuleViewSerializer
from places.models import Place, City
from users.serializer import PublicUserProfileSerializer, ReservationUserSerializer


class CreatePlaceSerializer(ModelSerializer):
    city = SlugRelatedField(queryset=City.objects.all(), slug_field='code')

    class Meta:
        model = Place
        fields = ["code", "type", "space", "max_guest", "city", "title"]
        read_only_fields = ('code',)


class PlaceListSerializer(ModelSerializer):
    space = SpaceSerializer()
    cover = ImageSerializer()
    city = CitySerializer()

    class Meta:
        model = Place
        fields = ["title", "code", "space", "city", "state", "max_guest", "price", "description", "cover", "summary", "rating", "rating_count"]


class PlaceUpdateSerializer(ModelSerializer):
    city = SlugRelatedField(queryset=City.objects.all(), slug_field='code')
    images = ImageSerializer(many=True, read_only=True)

    class Meta:
        model = Place
        fields = [ "title", "description", "type", "space", "max_guest",
                  "address_one", "address_two", "city", "state", "zip",
                  "amenities", "rules",
                  "beds", "baths", "checkin_from", "checkin_to", "checkout",
                  "min_stay", "max_stay", "price", "images", "published"]


class PlaceDetailSerializer(ModelSerializer):
    images = ImageSerializer(many=True)
    cover = ImageSerializer()
    type = TypeSerializer()
    space = SpaceSerializer()
    city = CitySerializer()
    amenities = AmenityViewSerializer(many=True)
    rules = RuleViewSerializer(many=True)
    host = SerializerMethodField()

    def get_host(self, place):

        if self.context.get("from_reservation"):
            return ReservationUserSerializer(place.host, context=self.context).data

        return PublicUserProfileSerializer(place.host, context=self.context).data

    class Meta:
        model = Place
        fields = ["code", "title", "description", "type", "space", "max_guest",
                  "address_one", "address_two", "city", "state", "zip",
                  "beds", "baths", "checkin_from", "checkin_to", "checkout",
                  "checkin_from_time", "checkin_to_time", "checkout_time",
                  "min_stay", "max_stay", "price", "images", "cover", "host",
                  "amenities", "rules", "rating", "rating_count"]



class PlaceSnapshotSerializer(ModelSerializer):
    images = ImageSerializer(many=True)
    cover = ImageSerializer()
    type = TypeSerializer()
    space = SpaceSerializer()
    city = CitySerializer()
    amenities = AmenityViewSerializer(many=True)
    rules = RuleViewSerializer(many=True)
    host = PublicUserProfileSerializer()

    class Meta:
        model = Place
        fields = ["code", "title", "description", "type", "space", "max_guest",
                  "address_one", "address_two", "city", "state", "zip",
                  "beds", "baths", "checkin_from", "checkin_to", "checkout",
                  "checkin_from_time", "checkin_to_time", "checkout_time",
                  "min_stay", "max_stay", "price", "images", "cover", "host",
                  "amenities", "rules" ]