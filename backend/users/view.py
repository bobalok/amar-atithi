from django.db.models.query_utils import Q
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.views import ObtainJSONWebToken

from users.models import User, UserToken, Documents
from users.serializer import UserRegisterSerializer, UserUpdateSerializer, PublicUserProfileSerializer, \
    CurrentUserSerializer, CreateVerificationRequestSerializer, DocumentSerializer


class IonObtainToken(ObtainJSONWebToken):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        if response.status_code == status.HTTP_200_OK:
            user = User.objects.get(email=request.data.get("email", ""))

            if user.email_code is not None:
                return Response("Email address is not verified", status=status.HTTP_406_NOT_ACCEPTABLE)

            if user.mobile_code is not None:
                return Response("Mobile verification required", status=status.HTTP_403_FORBIDDEN)

            if user.is_active is False:
                return Response("Your account has been disabled.", status=status.HTTP_410_GONE)

            user.last_login = timezone.now()
            user.save()

            usertoken = UserToken.objects.get(user=user)
            usertoken.token = response.data.get("token", None)
            usertoken.save()

        return response


class AdminObtainToken(ObtainJSONWebToken):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        if response.status_code == status.HTTP_200_OK:
            user = User.objects.get(email=request.data.get("email", ""))

            if user.is_superuser is False:
                return Response("You don't have permission to access this page", status=status.HTTP_403_FORBIDDEN)

            user.last_login = timezone.now()
            user.save()

            usertoken = UserToken.objects.get(user=user)
            usertoken.token = response.data.get("token", None)
            usertoken.save()

        return response

class UserRegisterView(CreateAPIView):
    serializer_class = UserRegisterSerializer
    queryset = User.objects.all()
    permission_classes = []


class VerifyEmailView(APIView):
    permission_classes = []

    def post(self, request, *args, **kwargs):
        email = request.data.get("email", "")
        code = request.data.get("code", "")

        user = User.objects.filter(email=email).first()

        if user:

            if user.email_code is None:
                return Response("Your email is already verified", status=status.HTTP_202_ACCEPTED)

            elif user.email_code == code:
                user.email_code = None
                user.save()
                return Response("Congratulation! Your email address has been successfully verified.", status=status.HTTP_200_OK)

        return Response("This link is no longer valid", status=status.HTTP_400_BAD_REQUEST)



class VerifyPhoneView(APIView):
    permission_classes = []

    def post(self, request, *args, **kwargs):
        email = request.data.get("email", "")
        code = request.data.get("code", "")

        user = User.objects.filter(email=email).first()

        if user:

            if user.mobile_code is None:
                return Response("This phone is already verified", status=status.HTTP_202_ACCEPTED)

            elif user.mobile_code == code:
                user.mobile_code = None
                user.save()
                return Response("This phone has been verified", status=status.HTTP_200_OK)

        return Response("Bad Request", status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def current_user(request):
    user = request.user

    if not user.is_authenticated:
        return Response({'error': 'User doesn\'t exists'}, status=401)

    serializer = CurrentUserSerializer(user).data

    return Response({
        'data': serializer
    })



class SelfUpdateView(APIView):
    serializer_class = UserUpdateSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return Response(UserUpdateSerializer(request.user).data)

    def put(self, request, *args, **kwargs):

        data = request.data
        user = self.request.user

        if data.get("first_name", None) is None:
            return Response({'name': "First Name is required"}, status=status.HTTP_400_BAD_REQUEST)

        if data.get("last_name", None) is None:
            return Response({'name': "Last Name is required"}, status=status.HTTP_400_BAD_REQUEST)

        if data.get("nickname", None) is None:
            return Response({'name': "Nickname is required"}, status=status.HTTP_400_BAD_REQUEST)

        if data.get("email", None) is None:
            return Response({'email': "Email address is required"}, status=status.HTTP_400_BAD_REQUEST)

        email_check = User.objects.filter(email=data.get("email")).first()

        if email_check and email_check != user:
            return Response({'email': "Email address already in use"}, status=status.HTTP_400_BAD_REQUEST)

        user.first_name = data.get("first_name")
        user.last_name = data.get("last_name")
        user.nickname = data.get("nickname")
        user.email = data.get("email")
        user.mobile = data.get("mobile")
        user.address = data.get("address")
        user.bio = data.get("bio")

        user.save()

        return Response(UserUpdateSerializer(user).data, status=status.HTTP_200_OK)


class UserView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = PublicUserProfileSerializer
    lookup_url_kwarg = 'userid'
    lookup_field = 'userid'
    permission_classes = []


class SubmittedDocuments(APIView):
    serializer_class = DocumentSerializer
    permission_classes = [IsAuthenticated]


    def get(self, request):
        queryset = Documents.objects.filter(Q(user=self.request.user)).order_by("-created_at").first()

        if queryset:
            return Response(DocumentSerializer( queryset, context=self.get_renderer_context()).data)
        return Response("")


class SubmitVerificationDocuments(CreateAPIView):
    queryset = Documents.objects.all()
    serializer_class = CreateVerificationRequestSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):

        if self.request.user.verified:
            raise ValidationError("You are already verified")

        return serializer.save(user=self.request.user)



#
# class UserListView(ListAPIView):
#     permission_classes = [IsAuthenticated, IsSuperUser]
#     serializer_class = UserSerializer
#     queryset = User.objects.all()
#
#
#
#

#
#
#
# class UserUpdateView(RetrieveUpdateAPIView):
#     serializer_class = UserUpdateSerializer
#     queryset = User.objects.all()
#     permission_classes = [IsAuthenticated, IsSuperUser]
#
#
# class SoftDeleteUser(UpdateAPIView):
#     serializer_class = UserSerializer
#     queryset = User.objects.all()
#     permission_classes = [IsAuthenticated, IsSuperUser]
#
#
#     def update(self, request, *args, **kwargs):
#         user = get_object_or_404(User, pk=kwargs.get("pk"))
#         user.is_active = False
#         user.save()
#
#         return Response(UserSerializer(user).data)
#
#
# def validateEmail(email):
#     from django.core.validators import validate_email
#     from django.core.exceptions import ValidationError
#     try:
#         validate_email(email)
#         return True
#     except ValidationError:
#         return False
#
#
# def SendResetLink(user, request):
#     # 0 == user not found
#     # 1 = success
#     # 2 = already verified
#
#     try:
#
#         link = "{}/reset/{}/{}".format(HOME_URL, user.username, user.reset_code)
#         htmly = get_template('reset-link.html')
#
#         context = {
#             'home': HOME_URL,
#             'logo': media_url("images/logo.png"),
#             'link': link,
#             'receiver': user.name
#         }
#
#         subject, from_email, to = 'Reset ESD Password', EMAIL_HOST_USER, user.email
#         # text_content = plaintext.render(d)
#         html_content = htmly.render(context)
#         text_content = 'Hi {},\n\r You have recently requested to reset your password. Please click the link below to reset your password: - {}\r\rThanks.' \
#             .format(user.name, link)
#         msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
#         msg.attach_alternative(html_content, "text/html")
#         msg.send()
#
#         print(msg)
#
#         return 1
#     except Exception as e:
#         print(str(e))
#         return 0
#
#
# def SendNewPassword(user, password, request):
#
#     try:
#
#         htmly = get_template('new-password.html')
#
#         context = {
#             'home': HOME_URL,
#             'logo': media_url("images/logo.png"),
#             'password': password,
#             'receiver': user.name
#         }
#
#         subject, from_email, to = 'Reset ESD Password', EMAIL_HOST_USER, user.email
#         # text_content = plaintext.render(d)
#         html_content = htmly.render(context)
#         text_content = 'Hi {},\n\r Your new password is : - {}\r\rThanks.' \
#             .format(user.name, password)
#         msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
#         msg.attach_alternative(html_content, "text/html")
#         msg.send()
#
#         return 1
#     except Exception as e:
#         print(str(e))
#         return 0
#
# class ResetPasswordView(APIView):
#     permission_classes = []
#
#     def post(self, request):
#         email = request.data.get("email")
#         reset_code = rand_str(6, True, True)
#
#         if validateEmail(email) == False:
#             return Response("Please enter a valid email", status=status.HTTP_406_NOT_ACCEPTABLE)
#
#         search = User.objects.filter(email=email)
#
#         if search.exists():
#             user = search.first()
#
#             user.reset_code = reset_code
#             user.save()
#
#             SendResetLink(user, request)
#         else:
#             return Response("This email doesn't belongs to anyone.", status=status.HTTP_406_NOT_ACCEPTABLE)
#
#
#         return Response("")
#
#
# class ValidateResetLink(APIView):
#     permission_classes = []
#
#     def post(self, request):
#         username = request.data.get("username")
#         code = request.data.get("code")
#         user = User.objects.get(username=username, reset_code=code)
#
#         if user is not None:
#             password = rand_str(6, True, False)
#
#             user.reset_code = None
#             user.set_password(password)
#             user.save()
#
#             SendNewPassword(user, password, request)
#
#         else:
#             return Response("This link is no longer valid", status=status.HTTP_406_NOT_ACCEPTABLE)
#
#         return Response("")
#
