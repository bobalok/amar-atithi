import json

from django.db import models
from django.forms import model_to_dict
from django.utils import timezone

from reservations.models import Reservation
from transactions.managers import InvoiceManager
from users.models import User


#
# class PAYMENT_STATUS:
#     VALID = 1
#     FAILED = 2
#     CANCELLED = 3

class Charges(models.Model):
    invoice = models.ForeignKey("transactions.Invoice", null=True, on_delete=models.CASCADE, related_name="invoice_charge_item")
    type = models.CharField(max_length=56, null=True, default=None)
    label = models.CharField(max_length=256, null=True, default=None)
    description = models.CharField(max_length=1024, null=True, default=None)
    amount = models.PositiveIntegerField(default=0)
    subtract = models.BooleanField(default=False, null=True)
    created_at = models.DateTimeField(blank=True, default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now, blank=True)


class Payment(models.Model):
    invoice = models.ForeignKey("Invoice", on_delete=models.SET_NULL, null=True, default=None, related_name="associated_invoice")
    status = models.CharField(max_length=56, null=True, default=None)
    tran_date = models.DateTimeField(null=True, default=None)
    tran_id = models.CharField(max_length=128, null=True, default=None)
    val_id = models.CharField(max_length=128, null=True, default=None)
    amount = models.DecimalField(default=0.0, max_digits=10, decimal_places=2, null=True)
    store_amount = models.DecimalField(default=0.0, max_digits=10, decimal_places=2, null=True)
    card_type = models.CharField(max_length=128, null=True, default=None)
    card_no = models.CharField(max_length=128, null=True, default=None)
    currency = models.CharField(max_length=128, null=True, default=None)
    bank_tran_id = models.CharField(max_length=128, null=True, default=None)
    card_issuer = models.CharField(max_length=128, null=True, default=None)
    card_brand = models.CharField(max_length=128, null=True, default=None)
    currency_type = models.CharField(max_length=128, null=True, default=None)
    currency_amount = models.DecimalField(default=0.0, max_digits=10, decimal_places=2, null=True)
    risk_level = models.IntegerField(null=True, default=None)
    risk_title = models.CharField(max_length=56, null=True, default=None)
    verified = models.BooleanField(default=False, null=True)


class Invoice(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, default=None)
    reservation = models.ForeignKey(Reservation, on_delete=models.SET_NULL, null=True, default=None,
                                    related_name="invoice_reservation")
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, default=None, null=True,
                                related_name="associated_payment")
    draft = models.BooleanField(default=True)
    refunded = models.BooleanField(default=False)
    refund_type = models.CharField(max_length=56, default=None, null=True)
    created_at = models.DateTimeField(blank=True, default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now, blank=True)
    objects = InvoiceManager()

    @property
    def charges(self):
        return Charges.objects.filter(invoice=self)

    @property
    def charges_details(self):
        from transactions.serializers import calculate_charges, parse_invoice_charges

        place_snapshot = self.reservation.place_snapshot
        place = json.loads(place_snapshot)
        price_per_night = int(place['price'])

        charges = self.charges.values('type', 'amount', 'subtract', 'label')
        parsed = parse_invoice_charges(price_per_night, self.reservation.nights, charges)

        return parsed

    @property
    def subtotal_without_credit(self):
        from transactions.serializers import calculate_payable_without_credit
        return calculate_payable_without_credit(self.charges_details)

    @property
    def subtotal(self):
        from transactions.serializers import calculate_payable
        return calculate_payable(self.charges_details)

    @property
    def receiveable(self):
        amount = 0.0

        for charge in self.charges_details:
            if charge.get("type") in ["RENT"]:
                amount = amount + charge.get("amount")

        return amount


class PaymentRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, default=None)
    method = models.CharField(max_length=56, null=True, default=None)
    amount = models.DecimalField(default=0.0, max_digits=10, decimal_places=2, null=True)
    number = models.CharField(max_length=128, null=True, default=None)
    status = models.CharField(max_length=56, default=0, null=True)