from django.urls import path

from places.views import UserListings
from reservations.views import BookingsList
from users.view import current_user, UserRegisterView, IonObtainToken, VerifyEmailView, VerifyPhoneView, SelfUpdateView, \
    UserView, SubmitVerificationDocuments, SubmittedDocuments, AdminObtainToken
from users.view_admin import DocumentsList, DocumentsDetail, ChangeDocumentVerdict

app_name = 'users'

urlpatterns = [

    # login
    path("auth", IonObtainToken.as_view()),
    path("admin-auth", AdminObtainToken.as_view()),
    path("", current_user),

    # register
    path("register", UserRegisterView.as_view(), name="register"),
    path("verify-email", VerifyEmailView.as_view(), name="verify-email"),
    path("verify-phone", VerifyPhoneView.as_view(), name="verify-phone"),

    path("update", SelfUpdateView.as_view()),
    path("details/<userid>", UserView.as_view()),
    # path("list", UserListView.as_view(), name="list"),
    # path("details/<username>", UserView.as_view()),
    # path("update/<username>/", UserUpdateView.as_view()),
    # path("delete/<username>", SoftDeleteUser.as_view()),
    # path("reset-password", ResetPasswordView.as_view()),
    # path("verify-reset-link", ValidateResetLink.as_view()),
    path("verification-requests", SubmittedDocuments.as_view()),
    path("request-verification", SubmitVerificationDocuments.as_view()),

    #user dashboard items
    path("listings/<userid>", UserListings.as_view()),
    path("bookings", BookingsList.as_view()),

    path("list-of-documents", DocumentsList.as_view()),
    path("documents/details/<pk>", DocumentsDetail.as_view()),
    path("documents/change-verdict", ChangeDocumentVerdict.as_view()),
]
