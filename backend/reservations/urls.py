from django.urls.conf import path

from places.components.views import ReviewAGuestView, ReviewTripView
from reservations.views import CheckAvailabilityView, CreateDraftReservation, ConfirmReservationView, \
    ReservationDetails, ReservationsList, AcceptReservationView, \
    RejectReservationView, GetPaymentUrl, PaymentCompleteView, IPNListener, ReservationAdjustmentQuote, \
    RequestReservationAdjustment, ReservationAdjustments, ReservationAdjustmentsDetails, GetAdjustmentPaymentURL, \
    AdjustmentPaymentCompleteView, CancelAdjRequest, AcceptAdjRequest, CanRequestAdjustment, PayWithCredit, \
    CancelReservationView

app_name = 'reservations'

urlpatterns = [
    path("", ReservationsList.as_view()),
    path("get-a-quote", CheckAvailabilityView.as_view()),
    path("create", CreateDraftReservation.as_view()),
    path("confirm-reservation/<ref>", ConfirmReservationView.as_view()),
    path("get-payment-url", GetPaymentUrl.as_view()),
    path("payment-complete", PaymentCompleteView.as_view(), name='payment_success'),
    path("adjustment-complete", AdjustmentPaymentCompleteView.as_view(), name='adjustment_payment_success'),
    path("payment-ipn", IPNListener.as_view()),
    path("details/<ref>", ReservationDetails.as_view()),
    path("pay-with-credit/<ref>", PayWithCredit.as_view()),

    path("accept/<ref>", AcceptReservationView.as_view()),
    path("reject/<ref>", RejectReservationView.as_view()),
    path("cancel/<ref>", CancelReservationView.as_view()),

    path("adjustments/<ref>", ReservationAdjustments.as_view()),
    path("adjustments/cancel/<ref>", CancelAdjRequest.as_view()),
    path("adjustments/accept/<ref>", AcceptAdjRequest.as_view()),
    path("adjustments/<ref>/details", ReservationAdjustmentsDetails.as_view()),
    path("adjustments/<ref>/payment-url", GetAdjustmentPaymentURL.as_view()),
    path("get-adjustment-quote", ReservationAdjustmentQuote.as_view()),
    path("request-adjustment", RequestReservationAdjustment.as_view()),
    path("can-request-adjustment", CanRequestAdjustment.as_view()),

    path("review-your-guest", ReviewAGuestView.as_view()),
    path("review-your-trip", ReviewTripView.as_view()),
]
