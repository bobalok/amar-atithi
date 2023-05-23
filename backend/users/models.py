import datetime
import hashlib
import time

from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.db.models import Q
from django.db.models.signals import post_save
from django.dispatch.dispatcher import receiver
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from rest_framework.authtoken.models import Token

from src.lib import rand_str
from src.settings import FORMATTED_DATE
from .managers import CustomUserManager


class User(AbstractBaseUser, PermissionsMixin):
    userid = models.CharField(max_length=28, null=True, default=None)
    first_name = models.CharField(_('first name'), max_length=128, null=True, default="")
    last_name = models.CharField(_('last name'), max_length=128, null=True, default="")
    nickname = models.CharField(_('nickname'), max_length=256, null=True, default="")
    email = models.EmailField(_('email address'), unique=True)
    mobile = models.CharField(_('mobile'), max_length=24, unique=True)
    photo = models.CharField(_('photo'), max_length=1024)
    dob = models.DateField(default=None, null=True)
    gender = models.PositiveIntegerField(default=0)
    nationality = models.CharField(max_length=56, default=None, null=True)
    credit = models.FloatField(default=0.0)
    tsv = models.BooleanField(default=False)
    address = models.CharField(max_length=512, default=None, null=True)
    bio = models.CharField(max_length=1024, default=None, null=True)
    password = models.CharField(max_length=256, null=True, default="", blank=True)
    email_code = models.CharField(max_length=24, null=True, default="", blank=True)
    mobile_code = models.CharField(max_length=24, null=True, default="", blank=True)
    reset_code = models.CharField(max_length=24, null=True, default=None, blank=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    verified = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.nickname

    @property
    def fullname(self):
        return "{} {}".format(self.first_name, self.last_name)

    @property
    def name(self):
        return self.nickname if len(self.nickname) > 0 else self.fullname

    @property
    def joined(self):
        stamp = time.mktime(self.date_joined.timetuple())
        return datetime.datetime.fromtimestamp(stamp).strftime("%B %Y")

    @property
    def joined_date(self):
        stamp = time.mktime(self.date_joined.timetuple())
        return datetime.datetime.fromtimestamp(stamp).strftime(FORMATTED_DATE)

    @property
    def login(self):
        if self.last_login:
            stamp = time.mktime(self.last_login.timetuple())
            return datetime.datetime.fromtimestamp(stamp).strftime(FORMATTED_DATE)
        else:
            return None

    def avatar_url(self, email, size):
        url = 'https://secure.gravatar.com/avatar'
        default = 'mp'
        rating = 'g'
        hash = hashlib.md5(email.lower().encode('utf-8')).hexdigest()
        return '{url}/{hash}?s={size}&d={default}&r={rating}'.format(url=url, hash=hash, size=size, default=default,
                                                                     rating=rating)

    @property
    def avatar(self):
        return self.avatar_url(self.email, 300) if self.photo is None or len(self.photo) == 0 else self.photo

    @property
    def email_verified(self):
        return self.email_code is None or len(str(self.email_code)) == 0

    @property
    def mobile_verified(self):
        return self.mobile_code is None or len(str(self.mobile_code)) == 0

    @property
    def is_host(self):
        from places.models import Place
        return Place.objects.filter(Q(host=self)).exists()

    @property
    def documents(self):
        return Documents.objects.filter(user=self).order_by("-created_at").first()


class UserToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, default="")
    token = models.CharField(max_length=1024, null=True, default="")


# Create a cart for each user
@receiver(post_save, sender=User, dispatch_uid="create_user_token")
def on_user_create(sender, instance, created, **kwargs):
    if created:
        UserToken(user=instance, token=None).save()

        userid = rand_str(10, False, False, True)
        while User.objects.filter(userid=userid).exists():
            userid = rand_str(10, False, False, True)

        instance.userid = userid
        instance.save()


def user_documents_path(documents, filename):
    userid = documents.user.userid
    return 'user-documents/{}/{}'.format(userid, filename)


class Documents(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, default="")
    method = models.IntegerField(default=0, null=True, blank=True)
    nid_no = models.CharField(max_length=128, null=True, blank=True, default=None)
    passport_no = models.CharField(max_length=128, null=True, blank=True, default=None)
    nid = models.ImageField(upload_to=user_documents_path)
    passport = models.ImageField(upload_to=user_documents_path)
    status = models.IntegerField(default=0)
    notes = models.CharField(max_length=1000, default=None, null=True)
    created_at = models.DateTimeField(blank=True, default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now, blank=True)