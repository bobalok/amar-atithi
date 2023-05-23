import datetime
import time

from django.db import models
from django.db.models.query_utils import Q
from django.utils import timezone

from places.models import Place, Review
from src.lib import rand_str
from src.settings import FORMATTED_DATE
from users.models import User


class Reservation(models.Model):
    reference = models.CharField(max_length=128, default=None, null=True)
    place = models.ForeignKey(Place, on_delete=models.SET_NULL, null=True, default=None)
    place_snapshot = models.TextField(null=True, default=None)
    guest = models.ForeignKey(User, on_delete=models.CASCADE)
    checkin = models.DateField()
    checkout = models.DateField()
    guests = models.PositiveIntegerField(default=1)
    status = models.PositiveIntegerField(default=1)
    reason = models.CharField(max_length=512, null=True, default=None)
    wc_message = models.CharField(max_length=512, null=True, default=None)
    invoice = models.ForeignKey("transactions.Invoice", on_delete=models.SET_NULL, null=True, default=None, related_name="res_invoice")
    created_at = models.DateTimeField(blank=True, default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now, blank=True)


    class Meta:
        ordering = ['-created_at']

    @property
    def host_review(self):
        from places.components.serializers import ReviewSerializer
        review = Review.objects.filter(reservation=self, type=0).first()

        if review:
            return ReviewSerializer(review).data
        return False

    @property
    def guest_review(self):
        from places.components.serializers import ReviewSerializer
        review = Review.objects.filter(reservation=self, type=1).first()

        if review:
            return ReviewSerializer(review).data
        return False

    @property
    def nights(self):
        try:
            return (self.checkout - self.checkin).days
        except Exception as e:
            print(str(e))
            return 0

    @property
    def has_adjustment(self):
        return Adjustments.objects.filter(Q(reservation=self)).count() > 0


    @property
    def timeline(self):
        from datetime import datetime

        date_format = "%Y-%m-%d"
        checkin_date = datetime.strptime(self.checkin.strftime(date_format), date_format).date()
        checkout_date = datetime.strptime(self.checkout.strftime(date_format), date_format).date()
        today = datetime.now().date()

        # today 27, checkout was 25
        if (today - checkout_date).days >= 0:
            return 0

        # today 20, checkin_date was 21
        if (today - checkin_date).days < 0:
            return 2
        else:
            return 1

    def _get_unique_code(self):
        code = rand_str(10, False, True, True)
        while Reservation.objects.filter(reference=code).exists():
            code = rand_str(12, False, True, True)
        return code

    def save(self, *args, **kwargs):
        if self.reference is None or len(self.reference) == 0:
            self.reference = self._get_unique_code()

        super().save()


class Calendar(models.Model):
    place = models.ForeignKey(Place, on_delete=models.CASCADE, null=True, default=None, related_name="calendar_place")
    date = models.DateField(blank=True, default=timezone.now)
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE, null=True, default=None, related_name="calendar_invoice")


class Adjustments(models.Model):
    reference = models.CharField(max_length=128, default=None, null=True)
    type = models.PositiveIntegerField(default=0, null=True)
    ttype = models.CharField(max_length=128, default=None, null=True)
    original_start = models.DateField(default=None, null=True)
    original_end = models.DateField(default=None, null=True)
    original_guests = models.PositiveIntegerField(default=1)
    start = models.DateField(default=None, null=True)
    end = models.DateField(default=None, null=True)
    guests = models.PositiveIntegerField(default=1)
    status = models.PositiveIntegerField(default=0, null=True)
    confirmed = models.BooleanField(default=False)
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE, null=True, default=None, related_name="adjustment_res")
    invoice = models.ForeignKey("transactions.Invoice", on_delete=models.SET_NULL, null=True, default=None, related_name="res_adjustment_invoice")
    created_at = models.DateTimeField(blank=True, default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now, blank=True)

    def _get_unique_code(self):
        code = rand_str(10, False, True, True)
        while Reservation.objects.filter(reference=code).exists():
            code = rand_str(12, False, True, True)
        return code

    def save(self, *args, **kwargs):
        if self.reference is None or len(self.reference) == 0:
            self.reference = self._get_unique_code()

        super().save()

    @property
    def created_timestamp(self):
        return time.mktime(self.created_at.timetuple())

    @property
    def created(self):
        return datetime.datetime.fromtimestamp(self.created_timestamp).strftime(FORMATTED_DATE)

