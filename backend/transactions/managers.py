from django.contrib.auth.base_user import BaseUserManager
from django.db.models import Manager
from django.utils.translation import ugettext_lazy as _




class InvoiceManager(Manager):

    def create_draft_invoice(self, res, user, **extra_fields):
        from transactions.models import Charges

        changes = Charges.objects.filter(enable=True, auto=True, archived=False)

        inv = self.model(reservation=res, user=user, **extra_fields)
        inv.save()

        inv.charges.set(changes)
        inv.save()

        return inv
