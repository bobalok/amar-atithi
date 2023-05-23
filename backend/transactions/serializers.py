from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from transactions.models import Invoice, Charges, Payment, PaymentRequest


def parse_invoice_charges(price_per_night, nights, charges_list):
    output = []

    for charge in charges_list:
        type = charge.get("type", "")
        message = charge.get("label", "")

        if type == "RENT":
            message = "{} BDT x {} {}".format(price_per_night, nights, "night" if nights == 1 else "nights")
        elif type == "SERVICE_FEE":
            message = "Service Charge"
        elif type == "CREDIT":
            message = "Account Credit"
        elif type == "NEGATIVE_ADJUSTMENT":
            message = "Adjustment"
        elif type == "TAX":
            message = "Tax"

        charge['label'] = str(message)


    return charges_list


def calculate_charges(price_per_night, nights, guest):
    rent_cost = int(nights * price_per_night)
    service_fee = float(rent_cost) * 0.10
    tax = float(rent_cost) * 0.15
    guest_credit = float(guest.credit)  if guest.is_authenticated else 0.0
    useable_credit = 0.0

    charges_list = [
        {
            'amount': rent_cost,
            'subtract': False,
            'type': 'RENT',
        },
        {
            'amount': service_fee,
            'subtract': False,
            'type': 'SERVICE_FEE'
        },
        {
            'amount': tax,
            'subtract': False,
            'type': 'TAX'
        }
    ]

    if guest_credit > 0.0:
        useable_credit = min(guest_credit, (rent_cost + service_fee + tax))

        charges_list.append({
            'amount': useable_credit,
            'subtract': True,
            'type': 'CREDIT'
        })

    charges_so_far = rent_cost + service_fee - useable_credit
    adjusted_total = int(charges_so_far)
    adjustment = charges_so_far - adjusted_total

    if adjustment > 0.0:
        charges_list.append({
            'amount': adjustment,
            'subtract': True,
            'type': 'NEGATIVE_ADJUSTMENT'
        })

    return charges_list


def calculate_payable_without_credit(charges_list):
    payable = 0.0

    for charge in charges_list:
        if charge.get("type") == "CREDIT":
            pass
        elif charge.get("type") in ["NEGATIVE_ADJUSTMENT" ]:
            payable = payable - charge.get("amount")
        else:
            payable = payable + charge.get("amount")

    return payable

def calculate_payable(charges_list):
    payable = 0.0

    for charge in charges_list:
        if charge.get("type") in ["NEGATIVE_ADJUSTMENT", "CREDIT" ]:
            payable = payable - charge.get("amount")
        else:
            payable = payable + charge.get("amount")

    return payable

class PaymentPublicSerializer(ModelSerializer):
    class Meta:
        model = Payment
        fields = ["status", "tran_date", "tran_id", "amount", "card_issuer"]


class InvoicePublicSerializer(ModelSerializer):
    payment = PaymentPublicSerializer()

    class Meta:
        model = Invoice
        fields = ["payment", "charges_details", "subtotal", "subtotal_without_credit"]


class ChargesSerializer(ModelSerializer):
    class Meta:
        model = Charges
        fields = ["label", "description"]


class PaymentRequestSerializer(ModelSerializer):
    status = SerializerMethodField()

    class Meta:
        model = PaymentRequest
        fields = "__all__"

    def get_status(self, request):
        status = str(request.status)

        if status == "1":
            return {
                "text": "Complete",
                "color": "success",
                "code": request.status
            }

        elif status == "2":
            return {
                "text": "Declined",
                "color": "error",
                "code": request.status
            }

        return {
            "text": "Pending",
            "color": "warning",
            "code": request.status
        }