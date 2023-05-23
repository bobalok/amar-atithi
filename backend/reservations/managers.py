from django.db import models
from django.db.models import Q
import logging

def SendFullRefund(reservation):
    subtotal = reservation.invoice.subtotal
    credit_used = reservation.invoice.credit_used
    refundable = subtotal + credit_used
    guest = reservation.guest

    guest.credit = guest.credit + refundable
    guest.save()


def send_refund(reservation, type):
    from transactions.models import Charges

    refundable = 0.0
    invoice = reservation.invoice
    rent = Charges.objects.filter(Q(type="RENT") & Q(invoice=invoice)).first()
    service = Charges.objects.filter(Q(type="SERVICE_FEE") & Q(invoice=invoice)).first()
    tax = Charges.objects.filter(Q(type="TAX") & Q(invoice=invoice)).first()

    rent_charge = rent.amount if rent else 0.0
    service_charge = service.amount if service else 0.0
    tax_charge = tax.amount if tax else 0.0

    if type == "FULL":
        refundable = rent_charge + service_charge + tax_charge
    elif type == "SEMI":
        refundable = rent_charge + tax_charge
    elif type == "LITE":
        refundable = (rent_charge * 0.5) + (tax_charge * .5)

    logging.debug("Rent: {} + Service: {} = Refundable = {}".format(rent_charge, service_charge, refundable))


    guest = reservation.guest
    logging.debug("Guest Credit: {} ".format(guest.credit))
    guest.credit = guest.credit + refundable
    guest.save()

    invoice.refund_type = type
    invoice.refunded = True
    invoice.save()
