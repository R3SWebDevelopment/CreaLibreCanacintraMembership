from django.db import models
from django.utils.translation import ugettext as _
from django.contrib.postgres.fields import JSONField
from django.conf import settings


class Profile(models.Model):
    mobile_number = JSONField(default={})
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile',
    )
    notify_by_email = models.BooleanField(default=True)
    notify_by_sms = models.BooleanField(default=False)
