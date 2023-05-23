from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from sms.views import SendVerificationSms
from src.emails import SendVerificationMail
from src.lib import rand_str
from users.models import User, Documents


# publicly accessible data
class PublicUserProfileSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["userid", "fullname", "name", "bio", "avatar", "gender", "joined",
                  "is_host", "email_verified", "mobile_verified"]


class ReservationUserSerializer(PublicUserProfileSerializer):
    class Meta:
        model = User
        fields = PublicUserProfileSerializer.Meta.fields + ["email", "mobile"]


class CurrentUserSerializer(PublicUserProfileSerializer):
    class Meta:
        model = User
        fields = PublicUserProfileSerializer.Meta.fields + ["first_name", "last_name", "nickname", "email",
                                                            "mobile", "photo", "dob", "gender", "credit", "verified"]


class UserRegisterSerializer(ModelSerializer):
    # company = serializers.PrimaryKeyRelatedField(required=False, allow_null=True, default=None, queryset=Company.objects.all())

    class Meta:
        model = User
        fields = ["first_name", "last_name", "nickname", "email", "mobile", "dob", "gender", "password"]
        # read_only_fields = ('is_active', 'last_login')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password(validated_data['password'])
        user.email_code = rand_str(8, False, True, True)
        user.mobile_code = None
        #user.mobile_code = rand_str(8, False, True, True)
        user.save()

        SendVerificationMail(user)
        #SendVerificationSms(user)

        return user


class UserUpdateSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "nickname", "email", "mobile", "address", "bio", "photo", "avatar"]

    def update(self, user, validated_data):
        print(validated_data.get("password", None))

        if validated_data.get("password", None):
            user.set_password(validated_data['password'])
            del validated_data['password']

        return super().update(user, validated_data)


class CreateVerificationRequestSerializer(ModelSerializer):
    nid = serializers.ImageField(required=False)
    passport = serializers.ImageField(required=False)

    class Meta:
        model = Documents
        fields = ["nid_no", "passport_no", "nid", "passport", "status", "method" ]


class DocumentSerializer(ModelSerializer):
    method_detail = SerializerMethodField()

    class Meta:
        model = Documents
        fields = ["nid_no", "passport_no", "nid", "passport", "status", "method", "method_detail", "notes"]

    def get_method_detail(self, document):
        if document.method == 1:
            return "Government ID Card"

        if document.method == 2:
            return "Passport"

        return ""


class DocumentDetailSerializer(ModelSerializer):
    method_detail = SerializerMethodField()
    user = PublicUserProfileSerializer()

    class Meta:
        model = Documents
        fields = ["pk", "user", "nid_no", "passport_no", "nid", "passport", "status", "method", "method_detail", "notes"]

    def get_method_detail(self, document):
        if document.method == 1:
            return "Government ID Card"

        if document.method == 2:
            return "Passport"

        return ""