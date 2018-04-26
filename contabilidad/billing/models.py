from django.db import models
from django.contrib.postgres.fields import JSONField, ArrayField
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _
from utils.logs import build_log

from crum import get_current_user


class TicketParser(models.Model):
    name = models.CharField(null=False, blank=False, max_length=20)


class Store(models.Model):
    name = models.CharField(null=False, blank=False, max_length=250)
    parser = models.ForeignKey(TicketParser, null=False, related_name='store')


class Ticket(models.Model):
    store = models.ForeignKey(Store, null=False, related_name='ticket')
    created_at = models.DateTimeField(null=False, auto_now_add=True)
    updated_at = models.DateTimeField(null=True, auto_now=True)
    created_by = models.ForeignKey(User, null=False, related_name="tickets_created")
    updated_by = models.ForeignKey(User, null=True, related_name="tickets_updated")
    data = JSONField(null=False, default={})
    is_invoiced = models.BooleanField(default=False, null=False)
    log = ArrayField(JSONField(), null=False, default=[])

    def save(self, *args, **kwargs):
        user = get_current_user()

        if user is None or not user.is_authenticated:
            raise ValidationError(_('Need to be log into the system to create the ticket'))

        if self.pk is None:
            self.created_by = user
            self.log = [build_log(user, _('Created the ticket'))]
        else:
            self.updated_by = user
            self.log = self.log.append(build_log(user, _('Updated the ticket')))
            super(Ticket, self).save(*args, **kwargs)


class TicketImage(models.Model):
    image = models.ImageField(null=False, upload_to='billing/tickets')
    ticket = models.ForeignKey(Ticket, null=False, related_name='images')