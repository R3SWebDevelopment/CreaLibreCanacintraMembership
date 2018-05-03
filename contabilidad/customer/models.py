from django.db import models
from django.utils.translation import ugettext as _
from django.contrib.postgres.fields import JSONField
from django.utils.functional import cached_property
from django.contrib.auth.models import User
from membership.models import MembershipRequest, Member, UpdateRequest


class Company(models.Model):
    full_name = models.CharField(max_length=250, null=False, blank=False, verbose_name=_('Company name'))
    rfc = models.CharField(max_length=13, name=False, blank=False, unique=True, verbose_name=_('Tax ID'),
                           help_text=_('Use the following format XXX[X]999999XXX'))
    address = JSONField(default={}, null=True)
    collaborators = models.ManyToManyField(User, related_name='companies', verbose_name=_('Collaborators'))
    has_membership = models.BooleanField(default=False)
    membership_has_expired = models.BooleanField(default=False)
    expiration_date = models.DateField(null=True, default=None)

    @cached_property
    def has_membership_request(self):
        return self.membership_request is not None

    @cached_property
    def is_member(self):
        return self.membership is not None

    @cached_property
    def membership(self):
        return Member.objects.filter(rfc=self.rfc).first()

    @cached_property
    def membership_request(self):
        return MembershipRequest.objects.filter(rfc=self.rfc).first()

    @cached_property
    def can_request_membership(self):
        return not self.is_member

    @cached_property
    def can_request_update(self):
        return self.is_member

    @cached_property
    def update_membership_request(self):
        return UpdateRequest.objects.filter(rfc=self.rfc).first()

    @cached_property
    def has_update_membership_request(self):
        return self.update_membership_request is not None

    @cached_property
    def can_renew(self):
        return self.is_member

    @cached_property
    def has_payment(self):
        return False

    class Meta:
        ordering = ['rfc']

    def __str__(self):
        return "{} - {}".format(self.rfc, self.full_name)

    def __unicode__(self):
        return u"{} - {}".format(self.rfc, self.full_name)
