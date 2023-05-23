from django.http.response import HttpResponse
from rest_framework.fields import SerializerMethodField
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer
from rest_framework.views import APIView

from places.models import Place, Image
import logging

logger = logging.getLogger()


def Home(self):
    return HttpResponse("Hello World")

class TestView( APIView ):
    permission_classes = []

    def get(self, request, *args, **kwargs):

        print("Hello Message")
        return Response("Hello World")


