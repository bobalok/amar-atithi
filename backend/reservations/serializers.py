"""
Status: 0: Discarded            :   Guest discarded a draft reservation
        1: Draft                :   Guest started the reservation process but haven't completed yet
        2: Payment Failed       :   Payment failed by customers bank
        3: Payment Cancelled    :   Payment cancelled by the user
        4: Payment Complete     :   Payment complete by the user but not verified by IPN
        5: Payment Confirmed    :   Payment confirmed by IPN
        6: Payment Rejected     :   Payment rejected by IPN. Potential fraud
        7: Pending              :   Payment completed by the guest but haven't received any response from host
        8: Accepted             :   Accepted by host
        9: Declined             :   Declined by host
        10: Expired              :   Host didn't respond
        11: Canceled             :   A host or guest canceled a confirmed reservation.
        12: Closed               :   Reservation cancelled by the system


Summary:    0-2 : No data will be visible to host's end. Place is unlocked and can be reserved by someone else
            3-5 : Place is locked and cannot be reserved by someone else
            6-9 : Place is unlocked and can be reserved again

"""
import json

from rest_framework.fields import SerializerMethodField
from rest_framework.relations import SlugRelatedField
from rest_framework.serializers import ModelSerializer

from places.components.serializers import ImageSerializer
from places.models import Place
from places.serializers import PlaceDetailSerializer, PlaceListSerializer
from reservations.models import Reservation, Adjustments
from transactions.serializers import InvoicePublicSerializer
from users.serializer import PublicUserProfileSerializer, ReservationUserSerializer




class ReservationStatus:
    DISCARDED = 0
    DRAFT = 1
    PAYMENT_FAILED = 2
    PAYMENT_CANCELLED = 3
    PAYMENT_COMPLETE = 4
    PAYMENT_CONFIRMED = 5 #deprecated
    PAYMENT_REJECTED = 6
    PENDING = 7
    ACCEPTED = 8
    DECLINED = 9
    EXPIRED = 10
    CANCELLED = 11
    CLOSED = 12
    COMPLETE = 13


def ReservationStatusList():
    return [
        {
            'id': ReservationStatus.DISCARDED,
            'text': 'Discarded'
        },
        {
            'id': ReservationStatus.DRAFT,
            'text': 'Draft'
        },
        {
            'id': ReservationStatus.PAYMENT_FAILED,
            'text': 'Payment Failed',
            'color': 'error'
        },
        {
            'id': ReservationStatus.PAYMENT_CANCELLED,
            'text': 'Cancelled',
            'color': 'error'
        },
        {
            'id': ReservationStatus.PAYMENT_COMPLETE,
            'text': 'Payment Verification Pending',
            'color': 'warning'
        },
        {
            'id': ReservationStatus.PAYMENT_REJECTED,
            'text': 'Payment Rejected',
            'color': 'error'
        },
        {
            'id': ReservationStatus.PENDING,
            'text': 'Pending',
            'color': 'warning'
        },
        {
            'id': ReservationStatus.ACCEPTED,
            'text': 'Accepted',
            'color': 'success'
        },
        {
            'id': ReservationStatus.DECLINED,
            'text': 'Declined',
            'color': 'error'
        },
        {
            'id': ReservationStatus.EXPIRED,
            'text': 'Expired',
            'color': 'error'
        },
        {
            'id': ReservationStatus.CANCELLED,
            'text': 'Canceled',
            'color': 'error'
        },
        {
            'id': ReservationStatus.CLOSED,
            'text': 'Closed',
            'color': 'error'
        },
        {
            'id': ReservationStatus.COMPLETE,
            'text': 'Complete',
            'color': 'success'
        },
    ]


def StatusSerializer(status):
    for x in ReservationStatusList():
        if x.get('id') == status:
            return x


class ReservationListSerializer(ModelSerializer):
    place = PlaceListSerializer()
    guest = PublicUserProfileSerializer()
    status = SerializerMethodField()

    def get_status(self, reservation):
        return StatusSerializer(reservation.status)

    class Meta:
        model = Reservation
        fields = ["reference", "place", "guest", "status", "checkin", "checkout", "guests", "nights", "created_at", "updated_at"]


class ReservationDetailSerializer(ModelSerializer):
    guest = ReservationUserSerializer()
    status = SerializerMethodField()
    invoice = InvoicePublicSerializer()
    place = SerializerMethodField()

    def get_place(self, reservation):
        return json.loads(reservation.place_snapshot)

    def get_status(self, reservation):
        return StatusSerializer(reservation.status)

    class Meta:
        model = Reservation
        fields = ["reference", "status", "place", "checkin", "checkout", "guests", "wc_message", "nights", "reason",
                  "timeline", "guest", "wc_message", "host_review", "guest_review", "invoice", "has_adjustment", "created_at", "updated_at"]


class DraftReservationCreateSerializer(ModelSerializer):
    place = SlugRelatedField(queryset=Place.objects.all(), slug_field='code')

    class Meta:
        model = Reservation
        fields = ["reference", "place", "checkin", "checkout", "guests", "created_at", "updated_at"]
        read_only_fields = ("reference",)


class ConfirmReservationSerializer(ModelSerializer):
    class Meta:
        model = Reservation
        fields = ["reference", "guests", "reason", "wc_message"]
        read_only_fields = ("reference",)


class ChangeReservationStatusSerializer(ModelSerializer):
    status = SerializerMethodField()

    def get_status(self, reservation):
        return StatusSerializer(reservation.status)

    class Meta:
        model = Reservation
        fields = ["status" ]


class AdjustmentsStatus:
    PENDING = 0
    ACCEPTED = 1
    REJECTED = 2
    CANCELLED = 3
    AUTO_CANCELLED = 4
    CONFIRMED = 5


def AdjustmentsStatusSerializer(status):
    if status == AdjustmentsStatus.PENDING:
        return {
            "text": "PENDING",
            "color": "warning",
            "code": status,
            "details": "Pending: Waiting for host's approval",
        }

    if status == AdjustmentsStatus.ACCEPTED:
        return {
            "text": "ACCEPTED",
            "color" : "success",
            "code": status,
            "details": "Accepted by Host",
        }

    if status == AdjustmentsStatus.REJECTED:
        return {
            "text": "REJECTED",
            "color": "error",
            "code": status,
            "details": "Rejected by Host",
        }

    if status == AdjustmentsStatus.CONFIRMED:
        return {
            "text": "CONFIRMED",
            "color" : "success",
            "code": status,
            "details": "Confirmed",
        }

    if status == AdjustmentsStatus.CANCELLED or status == AdjustmentsStatus.AUTO_CANCELLED:

        if status == AdjustmentsStatus.CANCELLED:
            details = "Cancelled by Guest"
        elif status == AdjustmentsStatus.AUTO_CANCELLED:
            details = "Cancelled by System"

        return {
            "text": "CANCELLED",
            "details": details,
            "color": "error",
            "code": status
        }

class AdjustmentSerializer(ModelSerializer):
    class Meta:
        model = Adjustments
        fields = ("reference", "created", "ttype", "original_start", "original_end", "start", "end", "status", "confirmed", "invoice", "created_at")


class AdjustmentPlaceSerializer(ModelSerializer):
    images = ImageSerializer(many=True)
    cover = ImageSerializer()
    host = SerializerMethodField()

    def get_host(self, place):
        return ReservationUserSerializer(place.host, context=self.context).data

    class Meta:
        model = Place
        fields = ["code", "title", "images", "cover", "host"]


class AdjustmentDetailSerializer(ModelSerializer):
    invoice = InvoicePublicSerializer()
    status = SerializerMethodField()
    place = SerializerMethodField()
    reservation = ReservationListSerializer()


    def get_status(self, adjustments):
        return AdjustmentsStatusSerializer(adjustments.status)

    def get_place(self, adjustments):
        return AdjustmentPlaceSerializer(adjustments.reservation.place, context=self.context).data

    class Meta:
        model = Adjustments
        fields = ("reference", "reservation", "created", "place", "ttype", "original_start", "original_end", "original_guests", "start", "end", "guests", "status", "confirmed", "invoice", "created_at")

