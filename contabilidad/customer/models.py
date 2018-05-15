from django.db import models
from django.utils.translation import ugettext as _
from django.contrib.postgres.fields import JSONField
from django.utils.functional import cached_property
from django.contrib.auth.models import User
from membership.models import MembershipRequest, Member, UpdateRequest
from membership.models import SAT_TAXPAYER_TYPE


class Company(models.Model):
    full_name = models.CharField(max_length=250, null=False, blank=False, verbose_name=_('Company name'))
    rfc = models.CharField(max_length=13, name=False, blank=False, unique=True, verbose_name=_('Tax ID'),
                           help_text=_('Use the following format XXX[X]999999XXX'))
    address = JSONField(default={}, null=True)
    collaborators = models.ManyToManyField(User, related_name='companies', verbose_name=_('Collaborators'))
    has_membership = models.BooleanField(default=False)
    membership_has_expired = models.BooleanField(default=False)
    expiration_date = models.DateField(null=True, default=None)
    product_service = models.ManyToManyField("ProductService", related_name='companies')
    certification = models.ManyToManyField("Certification", related_name='companies')
    sat_tax_payer_type = models.IntegerField(null=True, default=None, choices=SAT_TAXPAYER_TYPE)
    state = models.CharField(max_length=250, null=False, blank=True, verbose_name=_('State Name'))
    delegation = models.CharField(max_length=250, null=False, blank=True, verbose_name=_('Delegation Name'))

    @cached_property
    def product_services(self):
        return self.product_service.all()

    @cached_property
    def certifications(self):
        return self.certification.all()

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

    @cached_property
    def membership_status(self):
        return "En Proceso de Afiliación"

    @cached_property
    def branch_office(self):
        return "Ensenada"

    class Meta:
        ordering = ['rfc']

    def __str__(self):
        return "{} - {}".format(self.rfc, self.full_name)

    def __unicode__(self):
        return u"{} - {}".format(self.rfc, self.full_name)


class CompanyList(models.Model):
    code = models.CharField(max_length=10, null=False, blank=False)
    name = models.CharField(max_length=250, null=False, blank=False)

    class Meta:
        abstract = True
        ordering = ('code', 'name')

    def __str__(self):
        return "{} - {}".format(self.code, self.name)


class ProductService(CompanyList):
    pass


class Certification(CompanyList):
    pass
