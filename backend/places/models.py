import datetime
import os
import time

from django.db import models
from django.db.models import Q, Avg
from django.dispatch.dispatcher import receiver
from django.utils import timezone

from places.components.constants import checkin_times, checkout_times
from src.lib import rand_str
from src.settings import FORMATTED_DATE, media_url
from users.models import User


class Type(models.Model):
    name = models.CharField(max_length=128, null=True, default="")
    description = models.TextField(null=True, default="")
    order = models.PositiveIntegerField(default=0)
    deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(blank=True, default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now, blank=True)

    class Meta:
        ordering = ['order']


class Space(models.Model):
    name = models.CharField(max_length=128, null=True, default="")
    description = models.TextField(null=True, default="")
    created_at = models.DateTimeField(blank=True, default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now, blank=True)


class City(models.Model):
    name = models.CharField(max_length=128, null=True, default="")
    code = models.CharField(max_length=128, null=True, default="")
    created_at = models.DateTimeField(blank=True, default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now, blank=True)

    @property
    def states(self):
        return State.objects.filter(city=self)


class State(models.Model):
    name = models.CharField(max_length=128, null=True, default="")
    code = models.CharField(max_length=128, null=True, default="")
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    created_at = models.DateTimeField(blank=True, default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now, blank=True)


"""
=================== Amenity Model =======================
"""


class Amenity(models.Model):
    name = models.CharField(max_length=128, null=True, default="")
    description = models.CharField(max_length=256, null=True, default="")
    order = models.PositiveIntegerField(default=0)
    deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(blank=True, default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now, blank=True)

    class Meta:
        ordering = ['order', 'created_at']


"""
=================== Rules Model =======================
"""


class Rule(models.Model):
    name = models.CharField(max_length=128, null=True, default="")
    description = models.CharField(max_length=256, null=True, default="")
    order = models.PositiveIntegerField(default=0)
    deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(blank=True, default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now, blank=True)

    class Meta:
        ordering = ['order', 'created_at']


"""
=================== Place Model =======================
"""


class Place(models.Model):
    title = models.CharField(max_length=256, null=True, default="")
    description = models.CharField(max_length=2048, null=True, default="")
    code = models.CharField(max_length=128, null=True, default="")
    type = models.ForeignKey(Type, on_delete=models.SET_NULL, null=True, default=None)
    space = models.ForeignKey(Space, on_delete=models.SET_NULL, null=True, default=None)
    max_guest = models.PositiveIntegerField(default=1)
    address_one = models.CharField(max_length=512, default="", null=True)
    address_two = models.CharField(max_length=512, default="", null=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, default=None)
    state = models.CharField(max_length=512, default="", null=True)
    zip = models.PositiveIntegerField(default=None, null=True)
    host = models.ForeignKey(User, on_delete=models.CASCADE, null=True, default=None)
    beds = models.PositiveIntegerField(default=0)
    baths = models.PositiveIntegerField(default=0)
    amenities = models.ManyToManyField(Amenity, blank=True)
    rules = models.ManyToManyField(Rule, blank=True)
    checkin_from = models.PositiveIntegerField(default=0)
    checkin_to = models.PositiveIntegerField(default=0)
    checkout = models.PositiveIntegerField(default=0)
    min_stay = models.PositiveIntegerField(default=1)
    max_stay = models.PositiveIntegerField(default=0)
    price = models.PositiveIntegerField(default=0)
    deleted = models.BooleanField(default=False)
    published = models.BooleanField(default=False)
    reviews = models.ManyToManyField("places.Review", related_name='all_reviews')
    created_at = models.DateTimeField(blank=True, default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now, blank=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return self.title

    @property
    def rating_count(self):
        return Review.objects.filter(Q(reservation__place=self) & Q(type=0)).count()

    @property
    def rating(self):
        return Review.objects.filter(Q(reservation__place=self) & Q(type=0)).aggregate(Avg('rating'))['rating__avg']

    @property
    def images(self):
        return Image.objects.filter(place=self)

    @property
    def cover(self):
        images = Image.objects.filter(place=self)

        if not images.exists():
            return None

        cover = Image.objects.filter(place=self, cover=True)

        if cover.exists():
            return cover.first()
        else:
            return images.first()

    @property
    def summary(self):
        return self.description[0:175]

    @property
    def checkin_from_time(self):
        times = checkin_times()
        for time in times:
            if time.get('value') == self.checkin_from:
                return time.get("text")

        return ""

    @property
    def checkin_to_time(self):
        times = checkin_times()
        for time in times:
            if time.get('value') == self.checkin_to:
                return time.get("text")

        return ""

    @property
    def checkout_time(self):
        times = checkout_times()
        for time in times:
            if time.get('value') == self.checkout:
                return time.get("text")

        return ""

    @property
    def created_timestamp(self):
        return time.mktime(self.created_at.timetuple())

    @property
    def created(self):
        return datetime.datetime.fromtimestamp(self.created_timestamp).strftime(FORMATTED_DATE)

    def _get_unique_code(self):
        code = rand_str(10, False, False, True)
        while Place.objects.filter(code=code).exists():
            code = rand_str(10, False, False, True)
        return code

    def save(self, *args, **kwargs):
        if self.code is None or len(self.code) == 0:
            self.code = self._get_unique_code()

        super().save()


"""
=================== Image Model =======================
"""


def place_image_path(image, filename):
    code = image.place.code
    return 'place-images/{}/{}'.format(code, filename)


class Image(models.Model):
    file = models.ImageField(upload_to=place_image_path)
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    filename = models.CharField(max_length=512, null=True, default="")
    title = models.CharField(max_length=256, null=True, default="")
    description = models.CharField(max_length=512, null=True, default="")
    order = models.PositiveIntegerField(default=0)
    cover = models.BooleanField(default=False)
    size = models.IntegerField(default=0)
    type = models.CharField(max_length=12, null=True, blank=True, default=None)
    created_at = models.DateTimeField(blank=True, default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now, blank=True)

    class Meta:
        ordering = ['order', 'created_at']


@receiver(models.signals.pre_delete, sender=Image, dispatch_uid='place_image_ondelete')
def delete_file_on_placeimage_delete(sender, instance, **kwargs):
    if instance.file:
        if os.path.isfile(instance.file.path):
            os.remove(instance.file.path)


class Review(models.Model):
    reviewid = models.CharField(max_length=28, null=True, default=None)
    reservation = models.ForeignKey("reservations.Reservation", on_delete=models.CASCADE, null=True, default=None)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, default=None)
    rating = models.FloatField(default=0)
    review = models.CharField(max_length=2048, null=True, default=None)
    type = models.PositiveIntegerField(default=0)
    deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(blank=True, default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now, blank=True)

    def _get_unique_code(self):
        code = rand_str(10, False, True, True)
        while Review.objects.filter(reviewid=code).exists():
            code = rand_str(10, False, True, True)
        return code

    def save(self, *args, **kwargs):
        if self.reviewid is None or len(self.reviewid) == 0:
            self.reviewid = self._get_unique_code()

        super().save()

# class CustomAmenity(models.Model):
#     name = models.CharField(max_length=128, null=True, default="")
#     description = models.CharField(max_length=256, null=True, default="")
#     place = models.ForeignKey(Place, on_delete=models.CASCADE)
#     created_at = models.DateTimeField(blank=True, default=timezone.now)
#     updated_at = models.DateTimeField(default=timezone.now, blank=True)
#
#     class Meta:
#         ordering = ['created_at']
