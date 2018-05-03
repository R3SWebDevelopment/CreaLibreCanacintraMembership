from django.db import models
from django.utils.translation import ugettext as _
from django.contrib.postgres.fields import JSONField
from django.utils.functional import cached_property
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

    @cached_property
    def is_admin(self):
        return True if self.user.is_staff else False

    @cached_property
    def my_company(self):
        return self.user.companies.first()

    @cached_property
    def has_company(self):
        return self.my_company is not None

    @cached_property
    def comments(self):
        comments = []
        for comment in self.user.comments_sent.all():
            comments.append(comment)
        for comment in self.user.comments_received.all():
            comments.append(comment)
        return comments
