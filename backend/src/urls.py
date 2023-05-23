from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from src import settings
from src.views import TestView, Home

urlpatterns = [
    path("", Home),
    path('admin/', admin.site.urls),
    path('users/', include("users.urls", namespace="users-api")),
    path('places/', include("places.urls", namespace="place-api")),
    path('reservations/', include("reservations.urls", namespace="reservations-api")),
    path('transactions/', include("transactions.urls", namespace="transactions-api")),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)