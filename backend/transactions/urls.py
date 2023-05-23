from django.urls import path

from transactions.views import RequestPayment, RequestPaymentList, AllRequestPaymentList, RequestDetailView, \
    RequestUpdateView

app_name = 'transactions'

urlpatterns = [
    path("request-payment", RequestPayment.as_view()),
    path("payment-requests", RequestPaymentList.as_view()),
    path("payment-requests-list", AllRequestPaymentList.as_view()),
    path("payment-requests/<pk>", RequestDetailView.as_view()),
    path("update-payment-requests/<pk>", RequestUpdateView.as_view()),

]
