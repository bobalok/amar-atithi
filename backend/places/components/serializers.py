import ntpath
import os

from rest_framework.exceptions import ValidationError
from rest_framework.relations import SlugRelatedField
from rest_framework.serializers import ModelSerializer

from places.models import Type, Space, State, City, Image, Place, Amenity, Rule, Review


"""
=================== Type Serializer =======================
"""


class TypeSerializer(ModelSerializer):
    class Meta:
        model = Type
        fields = ["pk", "name", "description"]


class TypeDetailSerializer(ModelSerializer):
    class Meta:
        model = Type
        fields = ["pk", "name", "description", "order", "deleted"]


"""
=================== Space Serializer =======================
"""


class SpaceSerializer(ModelSerializer):
    class Meta:
        model = Space
        fields = ["name"]


class SpaceDetailSerializer(ModelSerializer):
    class Meta:
        model = Space
        fields = ["pk", "name", "description", ]



class AmenitySerializer(ModelSerializer):
    class Meta:
        model = Amenity
        fields = ["pk", "name", "description"]

class AmenityViewSerializer(ModelSerializer):
    class Meta:
        model = Amenity
        fields = [ "name", "description"]

class RuleSerializer(ModelSerializer):
    class Meta:
        model = Rule
        fields = ["pk", "name", "description"]


class RuleViewSerializer(ModelSerializer):
    class Meta:
        model = Rule
        fields = [ "name", "description"]

"""
=================== City and State Serializer =======================
"""


class CitySerializer(ModelSerializer):
    class Meta:
        model = City
        fields = ["name", "code"]


class StateSerializer(ModelSerializer):
    class Meta:
        model = State
        fields = ["name", "code"]


class StateDetailSerializer(ModelSerializer):
    city = CitySerializer()

    class Meta:
        model = State
        fields = ["name", "code", "city"]


class CityWithStateSerializer(ModelSerializer):
    states = StateSerializer(many=True)

    class Meta:
        model = City
        fields = ["name", "code", "states"]



"""
=================== Image Serializer =======================
"""

class ImageSerializer(ModelSerializer):
    class Meta:
        model = Image
        fields = [ "pk", "file", "title", "description"]


class UploadImageSerializer(ModelSerializer):
    place = SlugRelatedField(queryset=Place.objects.all(), slug_field='code')

    class Meta:
        model = Image
        fields = ('pk', 'file', 'place', 'title', 'description', 'order', 'cover', 'size', 'type')

    def create(self, validated_data):

        file_name = str(validated_data['file'])
        file_ext = os.path.splitext(file_name)[1].lower()
        file_size = int(validated_data['file'].size / 1024)
        max_allowed_size = 100 * 1024
        valid_extensions = ['.jpg', '.jpeg', ".png"]

        if not file_ext in valid_extensions:
            raise ValidationError(
                'The photo you selected cannot be uploaded. Please select a valid file. Allowed extensions are {}'
                    .format(", ".join(valid_extensions)))

        if file_size > max_allowed_size:
            raise ValidationError('The file you selected is too big. Maximum allowed size is 1 MB. '
                                  'Please compress the image before upload.')

        validated_data['filename'] = ntpath.basename(file_name)
        validated_data['title'] = ntpath.basename(file_name)
        validated_data['size'] = file_size
        validated_data['type'] = file_ext[1:]
        image_obj = Image.objects.create(**validated_data)

        return image_obj


"""
=================== Review Serializer =======================
"""


class ReviewSerializer(ModelSerializer):
    class Meta:
        model = Review
        fields = ["reviewid", "rating", "review", "type"]


class ReviewCreateSerializer(ModelSerializer):
    from reservations.models import Reservation
    reservation = SlugRelatedField( queryset=Reservation.objects.all(), slug_field='reference' )

    class Meta:
        model = Review
        fields = ["rating", "review", "reservation"]