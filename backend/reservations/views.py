import json
import logging
from datetime import datetime, timedelta, date

import requests
from django.db.models import Q
from django.http import HttpResponse
from django.http.response import JsonResponse, HttpResponseRedirect
from django.urls import reverse
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import CreateAPIView, UpdateAPIView, RetrieveAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from env import HOME_URL, SSLC_STORE_ID, SSLC_STORE_PASSWORD
from places.models import Place
from places.serializers import PlaceSnapshotSerializer
from reservations.managers import send_refund
from reservations.models import Reservation, Calendar, Adjustments
from reservations.permissions import NotReservationPlaceAuthor, IsReservationAuthorOrSu, CanViewReservation, \
    IsReservationPlaceAuthor
from reservations.serializers import DraftReservationCreateSerializer, ReservationDetailSerializer, ReservationStatus, \
    ConfirmReservationSerializer, ReservationListSerializer, ChangeReservationStatusSerializer, AdjustmentSerializer, \
    AdjustmentDetailSerializer, AdjustmentsStatus
from src.settings import ORDER_VALIDATION_ENDPOINT, SESSION_API
from transactions.models import Invoice, Charges, Payment

logger = logging.getLogger()


class ReservationsList(ListAPIView):
    serializer_class = ReservationListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Reservation.objects.filter(Q(place__host=self.request.user) & Q(status__gte=ReservationStatus.PENDING))


class BookingsList(ListAPIView):
    serializer_class = ReservationListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Reservation.objects.filter(Q(guest=self.request.user) & Q(status__gte=ReservationStatus.PENDING))


def CanBeReserved(request, code, checkin, checkout):
    try:

        place = Place.objects.get(code=code)
        date_format = "%Y-%m-%d"
        checkin_date = datetime.strptime(checkin, date_format).date()
        checkout_date = datetime.strptime(checkout, date_format).date()
        today_date = datetime.today().date()
        date_diff = (checkin_date - today_date).days
        night_stay = (checkin_date - today_date).days
        total_night = (checkout_date - checkin_date).days

        if request.user == place.host:
            return {"available": False, "message": "You cannot reserve your own place"}

        na = {"available": False, "message": "This place isn't available on the following date"}

        # user needs to book at least 1 day before
        if date_diff <= 0:
            return na

        print(night_stay)

        if total_night < max(place.min_stay, 1):
            return {"available": False, "message": "You have stay at least {} nights".format(max(place.min_stay, 1))}

        if total_night > max(place.max_stay, 1):
            return {"available": False,
                    "message": "You cannot stay more than {} nights in this place".format(max(place.max_stay, 1))}

        # checkin_dt = datetime.strptime(checkin, date_format)
        # checkout_dt = datetime.strptime(checkout, date_format)
        # checkout_night_dt = checkout_dt - timedelta(days=1)
        # checkout_night = checkout_night_dt.strftime(date_format)

        existings = Calendar.objects.filter(date__range=[checkin, checkout], place=place)

        if existings.exists():
            return na

        from transactions.serializers import calculate_charges, calculate_payable, parse_invoice_charges

        charges = calculate_charges(place.price, total_night, guest=request.user)
        parsed_message = parse_invoice_charges(place.price, total_night, charges)
        total = calculate_payable(charges)

        response = {
            'subtotal': total,
            'breakdown': parsed_message,
            "available": True
        }

        return response
    except Exception as e:
        logger.debug("Reservation Error: " + str(e))
        return {"available": False, "message": "Something went wrong, please try another place or date"}


class CheckAvailabilityView(APIView):
    permission_classes = []

    def post(self, request, *args, **kwargs):
        code = request.data.get("place")
        checkin = request.data.get("checkin")
        checkout = request.data.get("checkout")

        res = CanBeReserved(request, code, checkin, checkout)

        return Response(res)


class CreateDraftReservation(CreateAPIView):
    serializer_class = DraftReservationCreateSerializer
    queryset = Reservation.objects.all()
    permission_classes = [IsAuthenticated, NotReservationPlaceAuthor]

    def create(self, request, *args, **kwargs):
        code = request.data.get("place")
        checkin = request.data.get("checkin")
        checkout = request.data.get("checkout")

        res = CanBeReserved(request, code, checkin, checkout)

        if res.get('available') is False:
            return Response(res, status=status.HTTP_406_NOT_ACCEPTABLE)

        if request.user.is_authenticated is False:
            return Response({"available": False, "message": "Please login in order to make a reservation"}, status=status.HTTP_406_NOT_ACCEPTABLE)

        if request.user.verified is False:
            return Response({"available": False, "message": "You need to verify your account before making a reservation."}, status=status.HTTP_406_NOT_ACCEPTABLE)

        place = Place.objects.get(code=code)

        # delete if the user have any draft reservation of the same place
        Reservation.objects.filter(
            Q(guest=self.request.user) & Q(place__code=code) & Q(status=ReservationStatus.DRAFT)).delete()

        snapshot = JsonResponse(
            PlaceSnapshotSerializer(place, context=self.get_renderer_context()).data, safe=False
        ).content.decode("utf-8")

        reservation = Reservation()
        reservation.place = place
        reservation.place_snapshot = snapshot
        reservation.checkin = checkin
        reservation.checkout = checkout
        reservation.guests = request.data.get("guests", 1)
        reservation.guest = self.request.user
        reservation.save()

        inv = Invoice()
        inv.user = request.user
        inv.reservation = reservation
        inv.save()

        breakdown = res.get("breakdown")

        for breakdown_item in breakdown:
            inv_charge = Charges()
            inv_charge.type = breakdown_item.get("type")
            inv_charge.amount = breakdown_item.get("amount")
            inv_charge.subtract = breakdown_item.get("subtract")
            inv_charge.invoice = inv
            inv_charge.save()

        reservation.invoice = inv
        reservation.save()

        return Response(DraftReservationCreateSerializer(reservation).data)

    def perform_create(self, serializer):
        return serializer.save(status=ReservationStatus.DRAFT, guest=self.request.user)


class ConfirmReservationView(UpdateAPIView):
    serializer_class = ConfirmReservationSerializer
    queryset = Reservation.objects.all()
    permission_classes = [IsAuthenticated, IsReservationAuthorOrSu]
    lookup_url_kwarg = 'ref'
    lookup_field = 'reference'


class GetPaymentUrl(APIView):
    def post(self, request, *args, **kwargs):
        url = SESSION_API
        PAYMENT_COMPLETE_URL = request.build_absolute_uri(reverse("reservations:payment_success"))

        rrf = request.data.get("reservation")
        reservation = Reservation.objects.filter(reference=rrf)

        if reservation.exists() is False:
            return HttpResponse("Reservation doesn't exists")

        reservation = reservation.first()

        params = {
            'store_id': SSLC_STORE_ID,
            'store_passwd': SSLC_STORE_PASSWORD,
            'total_amount': reservation.invoice.subtotal,
            'currency': 'BDT',
            'tran_id': rrf,
            'success_url': PAYMENT_COMPLETE_URL,
            'fail_url': PAYMENT_COMPLETE_URL,
            'cancel_url': PAYMENT_COMPLETE_URL,
            'emi_option': '0',
            'cus_name': request.user.name,
            'cus_email': request.user.email,
            'cus_add1': 'Dhaka',
            'cus_add2': 'Dhaka',
            'cus_city': 'Dhaka',
            'cus_state': 'Dhaka',
            'cus_postcode': '1000',
            'cus_country': 'Bangladesh',
            'cus_phone': request.user.mobile,
            'shipping_method': "NO",
            'product_name': reservation.place.title,
            'product_category': reservation.place.type.pk,
            'product_profile': reservation.place.code,
            'value_a': "RESERVATION",
            # 'value_b ': 'ref002',
            # 'value_c': 'ref003',
            # 'value_d': 'ref004',
        }

        # # CART PARAMETERS
        # $post_data['cart'] = json_encode(array(
        #     array("product"=>"DHK TO BRS AC A1","amount"=>"200.00"),
        #     array("product"=>"DHK TO BRS AC A2","amount"=>"200.00"),
        #     array("product"=>"DHK TO BRS AC A3","amount"=>"200.00"),
        #     array("product"=>"DHK TO BRS AC A4","amount"=>"200.00")
        # ));

        # 'product_amount' : '100',
        # 'vat' : '5',
        # 'discount_amount' : '5',
        # 'convenience_fee' : '3',

        # print(params)

        response = requests.post(url, data=params)

        return HttpResponse(response.json()['GatewayPageURL'])


class PaymentCompleteView(APIView):
    permission_classes = []

    def get(self, request):
        return HttpResponseRedirect(redirect_to=HOME_URL)

    def post(self, request):
        tran_id = request.data.get("tran_id")
        reservation = Reservation.objects.filter(reference=tran_id)

        if reservation.exists():
            reservation = reservation.first()
            status = request.data.get("status")

            if status == "VALID":
                pass
            elif status == "FAILED":
                reservation.status = ReservationStatus.PAYMENT_FAILED
            else:
                reservation.status = ReservationStatus.PAYMENT_CANCELLED

            reservation.save()

            returnUrl = "{}/dashboard/reservations/{}".format(HOME_URL, tran_id)

            return HttpResponseRedirect(redirect_to=returnUrl)

        return HttpResponseRedirect(redirect_to=HOME_URL)


def VerifyReservationPayment(request):
    tran_id = request.data.get("tran_id")
    val_id = request.data.get("val_id")
    reservation = Reservation.objects.filter(reference=tran_id)

    logger.debug("IPN POST Request Received")

    if reservation.exists() is False:
        logger.debug("IPN reservation doesn't exists")

    if reservation.exists():
        reservation = reservation.first()

        payment = Payment()
        payment.invoice = reservation.invoice
        payment.status = request.data.get("status")
        payment.tran_date = request.data.get("tran_date")
        payment.tran_id = request.data.get("tran_id")
        payment.val_id = request.data.get("val_id")
        payment.amount = request.data.get("amount")
        payment.store_amount = request.data.get("store_amount")
        payment.card_type = request.data.get("card_type")
        payment.card_no = request.data.get("card_no")
        payment.currency = request.data.get("currency")
        payment.bank_tran_id = request.data.get("bank_tran_id")
        payment.card_issuer = request.data.get("card_issuer")
        payment.card_brand = request.data.get("card_brand")
        payment.currency_type = request.data.get("currency_type")
        payment.currency_amount = request.data.get("currency_amount")
        payment.risk_level = request.data.get("risk_level")
        payment.risk_title = request.data.get("risk_title")
        payment.save()

        invoice = reservation.invoice
        invoice.payment = payment
        invoice.save()

        # IPN is useless for failed transaction

        params = {
            'val_id': val_id,
            'store_id': SSLC_STORE_ID,
            'store_passwd': SSLC_STORE_PASSWORD
        }

        response = requests.get(ORDER_VALIDATION_ENDPOINT, params=params)

        if response:
            res = response.json()
            status = res.get("status")

            logger.debug("IPN POST Request Status " + status)

            if status == "VALID" or status == "VALIDATED":
                reservation.status = ReservationStatus.PENDING
                reservation.save()

                payment.verified = True
                payment.status = "VALID"
                payment.save()

                logger.debug("IPN Reservation Verified " + str(ReservationStatus.PENDING))

                credit_charge = Charges.objects.filter(
                    Q(type="CREDIT") & Q(invoice=reservation.invoice)).first()

                if credit_charge:
                    credit_used = credit_charge.amount
                    guest = reservation.guest
                    guest.credit = guest.credit - credit_used
                    guest.save()

                start_date = reservation.checkin.toordinal()
                end_date = reservation.checkout.toordinal()

                for i in range(start_date, end_date):
                    Calendar.objects.create(date=date.fromordinal(i), place=reservation.place,
                                            reservation=reservation)

            else:
                reservation.status = ReservationStatus.PAYMENT_REJECTED
                reservation.save()

                payment.status = "INVALID_TRANSACTION"
                payment.save()


class IPNListener(APIView):
    permission_classes = []

    def get(self, request):
        logger.debug("IPN Get Request Received")
        return HttpResponseRedirect(redirect_to=HOME_URL)

    def post(self, request):

        try:
            transaction_type = request.data.get("value_a")

            if transaction_type == "RESERVATION":
                logger.debug("IPN TRANSACTION: RESERVATION")
                VerifyReservationPayment(request)
            elif transaction_type == "RESERVATION_ADJUSTMENT":

                adj_ref = request.data.get("tran_id")
                val_id = request.data.get("val_id")
                adjustment = Adjustments.objects.filter(reference=adj_ref)

                logger.debug("IPN POST Request Received")

                if adjustment.exists() is False:
                    logger.debug("IPN reservation adjustment doesn't exists")

                if adjustment.exists():
                    adjustment = adjustment.first()

                    payment = Payment()
                    payment.invoice = adjustment.invoice
                    payment.status = request.data.get("status")
                    payment.tran_date = request.data.get("tran_date")
                    payment.tran_id = request.data.get("tran_id")
                    payment.val_id = request.data.get("val_id")
                    payment.amount = request.data.get("amount")
                    payment.store_amount = request.data.get("store_amount")
                    payment.card_type = request.data.get("card_type")
                    payment.card_no = request.data.get("card_no")
                    payment.currency = request.data.get("currency")
                    payment.bank_tran_id = request.data.get("bank_tran_id")
                    payment.card_issuer = request.data.get("card_issuer")
                    payment.card_brand = request.data.get("card_brand")
                    payment.currency_type = request.data.get("currency_type")
                    payment.currency_amount = request.data.get("currency_amount")
                    payment.risk_level = request.data.get("risk_level")
                    payment.risk_title = request.data.get("risk_title")
                    payment.save()

                    invoice = adjustment.invoice
                    invoice.payment = payment
                    invoice.save()

                    # IPN is useless for failed transaction

                    params = {
                        'val_id': val_id,
                        'store_id': SSLC_STORE_ID,
                        'store_passwd': SSLC_STORE_PASSWORD
                    }

                    response = requests.get(ORDER_VALIDATION_ENDPOINT, params=params)

                    if response:
                        res = response.json()
                        status = res.get("status")

                        logger.debug("IPN POST Request Status " + status)

                        if status == "VALID" or status == "VALIDATED":
                            adjustment.status = AdjustmentsStatus.CONFIRMED
                            adjustment.save()

                            payment.verified = True
                            payment.status = "VALID"
                            payment.save()

                            logger.debug("IPN Reservation Adjustment Verified " + str(ReservationStatus.PENDING))

                            credit_charge = Charges.objects.filter(
                                Q(type="CREDIT") & Q(invoice=adjustment.invoice)).first()

                            if credit_charge:
                                credit_used = credit_charge.amount
                                guest = adjustment.reservation.guest
                                guest.credit = guest.credit - credit_used
                                guest.save()

                            reservation = adjustment.reservation
                            reservation.checkin = adjustment.start
                            reservation.checkout = adjustment.end
                            reservation.guests = adjustment.guests
                            reservation.save()

                            Calendar.objects.filter(reservation=reservation).delete()

                            start_date = adjustment.start.toordinal()
                            end_date = adjustment.end.toordinal()

                            for i in range(start_date, end_date):
                                Calendar.objects.create(date=date.fromordinal(i), place=reservation.place,reservation=reservation)

                        else:
                            payment.status = "INVALID_TRANSACTION"
                            payment.save()



        except Exception as e:
            logger.debug("IPN ERROR: " + str(e))

        return HttpResponse("")


class PayWithCredit(APIView):
    serializer_class = ReservationDetailSerializer
    queryset = Reservation.objects.all()
    permission_classes = [IsAuthenticated, CanViewReservation]
    lookup_url_kwarg = 'ref'
    lookup_field = 'reference'

    def post(self, request, *args, **kwargs):

        reservation = Reservation.objects.get(Q(reference=kwargs.get("ref")))

        if reservation.invoice.subtotal > 0 :
            return Response("Bad request", status=status.HTTP_400_BAD_REQUEST)

        payment = Payment()
        payment.invoice = reservation.invoice
        payment.tran_date = None
        payment.tran_id = None
        payment.val_id = None
        payment.amount = reservation.invoice.subtotal
        payment.store_amount = reservation.invoice.subtotal
        payment.card_type = None
        payment.card_no = None
        payment.currency = None
        payment.bank_tran_id = None
        payment.card_issuer = None
        payment.card_brand = None
        payment.currency_type = None
        payment.currency_amount = reservation.invoice.subtotal
        payment.risk_level = None
        payment.risk_title = None
        payment.verified = True
        payment.status = "VALID"
        payment.save()

        invoice = reservation.invoice
        invoice.payment = payment
        invoice.save()

        credit_charge = Charges.objects.filter(
            Q(type="CREDIT") & Q(invoice=reservation.invoice)).first()

        print(credit_charge)
        print(credit_charge is not None)

        if credit_charge is not None:
            print("Credit Charged : {}".format(credit_charge.amount))
            guest = reservation.guest
            guest.credit = guest.credit - credit_charge.amount
            guest.save()

        start_date = reservation.checkin.toordinal()
        end_date = reservation.checkout.toordinal()

        for i in range(start_date, end_date):
            Calendar.objects.create(date=date.fromordinal(i), place=reservation.place,
                                    reservation=reservation)

        reservation.status = ReservationStatus.PENDING
        reservation.save()

        return Response(ReservationDetailSerializer(reservation, context=self.get_renderer_context()).data)

class ReservationDetails(RetrieveAPIView):
    serializer_class = ReservationDetailSerializer
    queryset = Reservation.objects.all()
    permission_classes = [IsAuthenticated, CanViewReservation]
    lookup_url_kwarg = 'ref'
    lookup_field = 'reference'

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['from_reservation'] = True
        return context


class AcceptReservationView(UpdateAPIView):
    serializer_class = ChangeReservationStatusSerializer
    queryset = Reservation.objects.all()
    permission_classes = [IsAuthenticated, IsReservationPlaceAuthor]
    lookup_url_kwarg = 'ref'
    lookup_field = 'reference'

    def perform_update(self, serializer):
        return serializer.save(status=ReservationStatus.ACCEPTED)


class CancelReservationView(UpdateAPIView):
    serializer_class = ChangeReservationStatusSerializer
    queryset = Reservation.objects.all()
    permission_classes = [IsAuthenticated, IsReservationPlaceAuthor]
    lookup_url_kwarg = 'ref'
    lookup_field = 'reference'

    def update(self, request, *args, **kwargs):
        reservation = Reservation.objects.get(reference=kwargs.get("ref", ""))

        send_refund(reservation, "FULL")

        reservation.status = ReservationStatus.CANCELLED
        reservation.save()

        start_date = reservation.checkin.toordinal()
        end_date = reservation.checkout.toordinal()

        for i in range(start_date, end_date):
            Calendar.objects.filter(date=date.fromordinal(i), place=reservation.place, reservation=reservation).delete()

        return Response(ChangeReservationStatusSerializer(reservation).data)


class RejectReservationView(UpdateAPIView):
    serializer_class = ChangeReservationStatusSerializer
    queryset = Reservation.objects.all()
    permission_classes = [IsAuthenticated, IsReservationPlaceAuthor]
    lookup_url_kwarg = 'ref'
    lookup_field = 'reference'

    def update(self, request, *args, **kwargs):
        ref = kwargs.get("ref", "")
        reservation = Reservation.objects.get(reference=ref)

        send_refund(reservation, "FULL")

        reservation.status = ReservationStatus.DECLINED
        reservation.save()

        start_date = reservation.checkin.toordinal()
        end_date = reservation.checkout.toordinal()

        for i in range(start_date, end_date):
            Calendar.objects.filter(date=date.fromordinal(i), place=reservation.place, reservation=reservation).delete()

        return Response(ChangeReservationStatusSerializer(reservation).data)


def CanReuquestAdjustment(reference):
    reservation = Reservation.objects.filter(reference=reference)

    if reservation.exists() is False:
        return {
            'error': True,
            'message': "The following reservation doesn't exists"
        }

    reservation = reservation.first()
    adjustments = Adjustments.objects.filter(
        Q(reservation=reservation) & (Q(status=AdjustmentsStatus.PENDING) | Q(status=AdjustmentsStatus.ACCEPTED)))

    if adjustments.exists() is True:
        return {
            'error': True,
            'message': "You already have an accepted or pending changes. Please cancel the previous adjustment request in order to submit another one."
        }

    return {
        'error': False
    }


def ReservationAdjustment(reservation, start, end):
    place_snapshot = reservation.place_snapshot
    place = json.loads(place_snapshot)

    booked = Calendar.objects.filter(Q(date__range=[start, end]) & Q(place=reservation.place)).exclude(reservation=reservation)

    date_format = "%Y-%m-%d"
    start_date = datetime.strptime(start, date_format)
    end_date = datetime.strptime(end, date_format)
    today = datetime.now()
    isStarted = (start_date.date() - today.date()).days < 1
    start_date = start_date.date() if isStarted is False else reservation.checkin

    # if (start_date.date() - today.date()).days < 1:
    #     return {
    #         'error': True,
    #         'message': "Reservation starting date cannot be set to a past or present date"
    #     }

    if (end_date.date() - start_date).days < 1:
        return {
            'error': True,
            'message': "Incorrect input. Checkout and checkin time cannot be same or earlier."
        }

    if booked.exists():
        return {
            'error': True,
            'message': "The following dates are already reserved"
        }

    nights = (datetime.strptime(end, "%Y-%m-%d") - datetime.strptime(start, "%Y-%m-%d")).days
    diff_nights = abs(nights - reservation.nights)

    if nights > reservation.nights:
        unit_cost = place.get("price")
        total_cost = unit_cost * diff_nights
        service_fee = total_cost * 0.05
        tax = total_cost * .15
        subtotal = total_cost + service_fee + tax

        charges = [
            {
                'id': "RENT",
                'label': 'Rent fee for additional {} {}'.format(diff_nights,
                                                                "nights" if diff_nights > 1 else "night"),
                'unit_cost': unit_cost,
                'total_cost': total_cost
            },
            {
                'id': "SERVICE_FEE",
                'label': "Service Charge",
                'unit_cost': service_fee,
                'total_cost': service_fee
            },
            {
                'id': "TAX",
                'label': "15% Tax",
                'unit_cost': tax,
                'total_cost': tax
            }
        ]

        return {
            'error': False,
            'subtotal': subtotal,
            'type': 'DEBIT',
            'breakdown': charges
        }

    elif nights < reservation.nights:

        unit_cost = place.get("price")
        total_cost = unit_cost * diff_nights
        charges = [
            {
                'id': "RENT_FEE_CREDITED",
                'label': 'Rent fee refund for {} {}'.format(diff_nights, "nights" if diff_nights > 1 else "night"),
                'unit_cost': unit_cost,
                'total_cost': total_cost
            },
        ]

        return {
            'error': False,
            'subtotal': total_cost,
            'type': 'CREDIT',
            'breakdown': charges
        }

    else:
        return {
            'error': False,
            'subtotal': 0,
            'type': 'NONE',
            'breakdown': []
        }


class ReservationAdjustmentQuote(APIView):
    def post(self, request, *args, **kwargs):
        reference = request.data.get("reference")
        start = request.data.get("checkin")
        end = request.data.get("checkout")

        check = CanReuquestAdjustment(reference)

        if check.get("error") is True:
            return Response(check)

        reservation = Reservation.objects.get(reference=reference)
        adjustment = ReservationAdjustment(reservation, start, end)

        return Response(adjustment)


class RequestReservationAdjustment(APIView):
    def post(self, request, *args, **kwargs):
        reference = request.data.get("reference")
        start = request.data.get("checkin")
        end = request.data.get("checkout")
        guests = request.data.get("guests")

        check = CanReuquestAdjustment(reference)

        if check.get("error") is True:
            return Response(check)

        reservation = Reservation.objects.get(reference=reference)

        adjustment_result = ReservationAdjustment(reservation, start, end)

        if adjustment_result.get("error") is False:
            type = adjustment_result.get("type")
            charges = adjustment_result.get("breakdown")
            inv = None

            if type != "NONE":
                inv = Invoice()
                inv.user = request.user
                inv.reservation = reservation
                inv.payment = None
                inv.save()

                for charge in charges:
                    inv_charge = Charges()
                    inv_charge.invoice = inv
                    inv_charge.type = charge.get("id")
                    inv_charge.label = charge.get("label")
                    inv_charge.amount = charge.get("total_cost")
                    inv_charge.save()

            adjustment = Adjustments()
            adjustment.original_start = reservation.checkin
            adjustment.original_end = reservation.checkout
            adjustment.original_guests = reservation.guests
            adjustment.start = start
            adjustment.end = end
            adjustment.guests = guests
            adjustment.status = 0
            adjustment.reservation = reservation
            adjustment.invoice = inv
            adjustment.ttype = type
            adjustment.save()

            adjustment_result['adjustment'] = AdjustmentDetailSerializer(adjustment).data

        return Response(adjustment_result)


class ReservationAdjustments(ListAPIView):
    serializer_class = AdjustmentDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Adjustments.objects.filter(Q(reservation__reference=self.kwargs.get("ref"))).order_by("-created_at")


class ReservationAdjustmentsDetails(RetrieveAPIView):
    serializer_class = AdjustmentDetailSerializer
    permission_classes = [IsAuthenticated]
    queryset = Adjustments.objects.all()
    lookup_field = 'reference'
    lookup_url_kwarg = 'ref'


class GetAdjustmentPaymentURL(APIView):
    def post(self, request, *args, **kwargs):
        url = SESSION_API
        PAYMENT_COMPLETE_URL = request.build_absolute_uri(reverse("reservations:adjustment_payment_success"))

        ref = self.kwargs.get("ref")
        adjustment = Adjustments.objects.filter(Q(reference=ref))

        if adjustment.exists() is False:
            return Response({
                'error': True,
                'message': 'Adjustment doesn\'t exists'
            })

        adjustment = adjustment.first()
        reservation = adjustment.reservation

        if adjustment.ttype != "DEBIT" or adjustment.invoice.subtotal == 0:
            return Response({
                'error': True,
                'message': 'Payment not required'
            })

        if adjustment.status != AdjustmentsStatus.ACCEPTED:

            if adjustment.status == AdjustmentsStatus.PENDING:
                message = "Please wait till the request is accepted"
            elif adjustment.status == AdjustmentsStatus.CONFIRMED:
                message = "Adjustment is already confirmed"
            else:
                message = "This request has been declined"

            return Response({
                'error': True,
                'message': message
            })

        params = {
            'store_id': SSLC_STORE_ID,
            'store_passwd': SSLC_STORE_PASSWORD,
            'total_amount': adjustment.invoice.subtotal,
            'currency': 'BDT',
            'tran_id': adjustment.reference,
            'success_url': PAYMENT_COMPLETE_URL,
            'fail_url': PAYMENT_COMPLETE_URL,
            'cancel_url': PAYMENT_COMPLETE_URL,
            'emi_option': '0',
            'cus_name': request.user.name,
            'cus_email': request.user.email,
            'cus_add1': 'Dhaka',
            'cus_add2': 'Dhaka',
            'cus_city': 'Dhaka',
            'cus_state': 'Dhaka',
            'cus_postcode': '1000',
            'cus_country': 'Bangladesh',
            'cus_phone': request.user.mobile,
            'shipping_method': "NO",
            'product_name': reservation.place.title,
            'product_category': reservation.place.type.pk,
            'product_profile': reservation.place.code,
            'value_a': "RESERVATION_ADJUSTMENT",
            # 'value_b ': reservation.reference,
            # 'value_c': 'ref003',
            # 'value_d': 'ref004',
        }

        logger.debug("PRODUCT NAME" + reservation.place.title)

        response = requests.post(url, data=params)

        return Response({
            'error': False,
            'url': response.json()['GatewayPageURL']
        })


class AdjustmentPaymentCompleteView(APIView):
    permission_classes = []

    def get(self, request):
        return HttpResponseRedirect(redirect_to=HOME_URL)

    def post(self, request):
        tran_id = request.data.get("tran_id")
        adjustment = Adjustments.objects.filter(reference=tran_id)

        if adjustment.exists():
            adjustment = adjustment.first()
            reference = adjustment.reservation.reference
            returnUrl = "{}/dashboard/reservations/{}".format(HOME_URL, reference)

            return HttpResponseRedirect(redirect_to=returnUrl)

        return HttpResponseRedirect(redirect_to=HOME_URL)


class CancelAdjRequest(UpdateAPIView):
    serializer_class = AdjustmentDetailSerializer
    permission_classes = [IsAuthenticated]
    queryset = Adjustments.objects.all()
    lookup_field = 'reference'
    lookup_url_kwarg = 'ref'

    def update(self, request, *args, **kwargs):
        adjustment = Adjustments.objects.get(reference=self.kwargs.get("ref"))

        if adjustment.reservation.guest == request.user:
            adjustment.status = AdjustmentsStatus.CANCELLED
        elif adjustment.reservation.place.host == request.user:
            adjustment.status = AdjustmentsStatus.REJECTED

        adjustment.save()

        return Response(AdjustmentDetailSerializer(adjustment, context=self.get_renderer_context()).data)


class AcceptAdjRequest(UpdateAPIView):
    serializer_class = AdjustmentDetailSerializer
    permission_classes = [IsAuthenticated]
    queryset = Adjustments.objects.all()
    lookup_field = 'reference'
    lookup_url_kwarg = 'ref'

    def update(self, request, *args, **kwargs):
        adjustment = Adjustments.objects.get(reference=self.kwargs.get("ref"))

        if adjustment.ttype == "DEBIT":
            adjustment.status = AdjustmentsStatus.ACCEPTED
            adjustment.save()
        else:

            reservation = adjustment.reservation
            reservation.checkin = adjustment.start
            reservation.checkout = adjustment.end
            reservation.guests = adjustment.guests
            reservation.save()

            adjustment.status = AdjustmentsStatus.ACCEPTED
            adjustment.save()

            Calendar.objects.filter(reservation=reservation).delete()

            start_date = adjustment.start.toordinal()
            end_date = adjustment.end.toordinal()

            for i in range(start_date, end_date):
                Calendar.objects.create(date=date.fromordinal(i), place=reservation.place, reservation=reservation)

            if adjustment.ttype == "CREDIT":
                amount = adjustment.invoice.subtotal

                if amount > 0:
                    user = request.user
                    user.credit = user.credit + amount
                    user.save()

        return Response(AdjustmentDetailSerializer(adjustment, context=self.get_renderer_context()).data)


class CanRequestAdjustment(APIView):
    def post(self, request, *args, **kwargs):
        reference = request.data.get("reference")
        return Response(CanReuquestAdjustment(reference))
