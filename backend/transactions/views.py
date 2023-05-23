from django.shortcuts import render

# Create your views here.
from rest_framework.generics import ListAPIView, RetrieveAPIView, UpdateAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from src.permission import IsSuperUser
from transactions.models import PaymentRequest
from transactions.serializers import PaymentRequestSerializer


class RequestPayment(APIView):

    def post(self, request, *args, **kwargs):

        amount = float(request.data.get("amount"))
        user = request.user

        if user.credit >= amount:
            req = PaymentRequest()
            req.user = request.user
            req.method = request.data.get("method")
            req.amount = request.data.get("amount")
            req.number = request.data.get("number")
            req.status = 0
            req.save()

            user.credit = user.credit - amount
            user.save()

            return Response(PaymentRequestSerializer(req).data)
        else:
            return ValueError("Not enough balance")


class RequestPaymentList(ListAPIView):
    serializer_class = PaymentRequestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return PaymentRequest.objects.filter(user=self.request.user)



class AllRequestPaymentList(ListAPIView):
    serializer_class = PaymentRequestSerializer
    queryset = PaymentRequest.objects.all()
    permission_classes = [IsAuthenticated, IsSuperUser]


class RequestDetailView(RetrieveAPIView):
    serializer_class = PaymentRequestSerializer
    queryset = PaymentRequest.objects.all()
    permission_classes = [IsAuthenticated, IsSuperUser]



class RequestUpdateView(RetrieveUpdateAPIView):
    serializer_class = PaymentRequestSerializer
    queryset = PaymentRequest.objects.all()
    permission_classes = [IsAuthenticated, IsSuperUser]

    def update(self, request, *args, **kwargs):

        status = request.data.get("status", 0)

        paymentrequest = PaymentRequest.objects.get(pk=kwargs.get("pk"))
        paymentrequest.status = request.data.get("status", 0)
        paymentrequest.save()

        print(paymentrequest)

        if status == 2:
            user = paymentrequest.user
            amount = paymentrequest.amount
            user.credit = float(user.credit) + float(amount)
            user.save()

        return Response(PaymentRequestSerializer(paymentrequest, context=self.get_renderer_context()).data)