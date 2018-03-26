# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.postgres.fields import ArrayField, JSONField
from django.contrib.auth.models import User

SAT_PERSON_TYPE = 1
SAT_ORGANIZATION_TYPE = 2
SAT_TAXPAYER_TYPE = (
    (SAT_PERSON_TYPE, "Fisca"),
    (SAT_ORGANIZATION_TYPE, "Moral")
)

CUSTOM_ACTIVITY_IMPORT = 1
CUSTOM_ACTIVITY_EXPORT = 2
CUSTOM_ACTIVITY_CHOICE = (
    (CUSTOM_ACTIVITY_IMPORT, "Importa"),
    (CUSTOM_ACTIVITY_EXPORT, "Exporta"),
)

CONSTITUTIVE_ACT = "CONSTITUTIVE_ACT"
LEGAL_POWER = "LEGAL_POWER"
EMPLOYERS_FEED = "EMPLOYERS_FEED"
LEGAL_REPRESENTATIVE_OFFICIAL_ID = "LEGAL_REPRESENTATIVE_OFFICIAL_ID"
LAST_TAX_RETURN = "LAST_TAX_RETURN"
RFC = "RFC"
OFFICIAL_ID = "OFFICIAL_ID"
REGISTRATION_REGISTER = "REGISTRATION_REGISTER"
LAST_EMPLOYERS_FEED = "LAST_EMPLOYERS_FEED"

FILE_TYPE_CHOICES = (
    (CONSTITUTIVE_ACT, "Acta Constitutiva"),
    (LEGAL_POWER, "Poder Legal"),
    (EMPLOYERS_FEED, "Cuota Patronal"),
    (LEGAL_REPRESENTATIVE_OFFICIAL_ID, "Identificación Oficial del Representante Legal"),
    (LAST_TAX_RETURN, "Ultima declaración"),
    (RFC, "R.F.C."),
    (OFFICIAL_ID, "Identificación Oficial"),
    (REGISTRATION_REGISTER, "Inscripción del Padrón"),
    (LAST_EMPLOYERS_FEED, "Ultima cuota Patronal"),
)


def get_file_type_label(type):
    for t in FILE_TYPE_CHOICES:
        if t[0] == type:
            return t[1]
    return None

REQUIRED_FILES = {
    SAT_PERSON_TYPE: [
        OFFICIAL_ID,
        REGISTRATION_REGISTER,
        LAST_EMPLOYERS_FEED,
        LAST_TAX_RETURN,
        RFC
    ],
    SAT_ORGANIZATION_TYPE: [
        CONSTITUTIVE_ACT,
        LEGAL_POWER,
        EMPLOYERS_FEED,
        LEGAL_REPRESENTATIVE_OFFICIAL_ID,
        LAST_TAX_RETURN,
        RFC
    ]
}


class MemberInfo(models.Model):
    sat_taxpayer_type = models.IntegerField(null=True, default=None, choices=SAT_TAXPAYER_TYPE)
    business_name = models.CharField(max_length=250, null=True, default=None)
    trade_name = models.CharField(max_length=250, null=True, default=None)
    street_name_1 = models.CharField(max_length=250, null=True, default=None)
    street_number = models.CharField(max_length=10, null=True, default=None)
    apartment_number = models.CharField(max_length=10, null=True, default=None)
    suburb = models.CharField(max_length=250, null=True, default=None)
    zip_code = models.CharField(max_length=5, null=True, default=None)
    municipality = models.CharField(max_length=250, null=True, default=None)
    state = models.CharField(max_length=250, null=True, default=None)
    # phone Format [{"area_code":"999|99", "number": "9999-9999|999-9999", "extension":["99","999"]}]
    phone = ArrayField(JSONField())
    mobile = models.CharField(max_length=14, null=True, default=None)
    main_activity_description = models.CharField(max_length=250, null=True, default=None)
    scian_code = models.CharField(max_length=250, null=True, default=None)
    main_product_service = models.CharField(max_length=250, null=True, default=None)
    tariff_fraction = models.CharField(max_length=100, null=True, default=None)
    begins_operations = models.DateField(null=True, default=None)
    total_employees = models.IntegerField(null=True, default=None)
    gross_sell_range = models.DecimalField(null=True, default=None, max_digits=12, decimal_places=2)
    customs_activity = models.IntegerField(null=True, default=None, choices=CUSTOM_ACTIVITY_CHOICE)
    # CEO, legal representative, main representative Format:
    # {
    #   "name": "[FIRST NAME] [MIDDLE NAME] [LAST NAME]"
    #   "email": "address@domain",
    #   "area_code":"999|99",
    #   "number": "9999-9999|999-9999",
    #   "extension":["99","999"]
    # }
    ceo = JSONField()
    legal_representative = JSONField()
    main_representative = JSONField()
    # other representative have the same format as the CEO, legal representative and main representative plus additional
    # fields
    # {
    #   "area_name": "AAAAAA AAAAA AAAAA"
    # }
    other_representative = JSONField()
    website = models.URLField(null=True, default=None)

    class Meta:
        abstract = True

    @property
    def required_fields(self):
        return REQUIRED_FILES.get(int(self.sat_taxpayer_type)) if self.sat_taxpayer_type is not None else []


class AttachedFile(models.Model):
    type = models.CharField(max_length=100, choices=FILE_TYPE_CHOICES)
    file = models.FileField(upload_to="attachment")

    def __str__(self):
        label = get_file_type_label(self.type)
        return "{} - {}".format(label if label is not None else self.type, self.file.name)


class MembershipRequest(MemberInfo):
    created_at = models.DateTimeField(auto_now_add=True)
    requested_by = models.ForeignKey(User, related_name="membership_requests")
    requested_at = models.DateTimeField(null=True, default=None)
    attended_by = models.ForeignKey(User, related_name="membership_requests_approved")
    validated = models.NullBooleanField(null=True, default=None)
    member = models.OneToOneField("Member", related_name="request")
    attachment = models.ManyToManyField(AttachedFile)

    def __str__(self):
        return "{} - {}".format(self.requested_by, self.created_at)


class UpdateRequest(MemberInfo):
    member = models.OneToOneField("Member", related_name="update_requests")
    created_at = models.DateTimeField(auto_now_add=True)
    requested_by = models.ForeignKey(User, related_name="update_requests")
    requested_at = models.DateTimeField(null=True, default=None)
    attended_by = models.ForeignKey(User, related_name="update_requests_approved")
    validated = models.NullBooleanField(null=True, default=None)

    def __str__(self):
        return "{} - {} - {}".format(self.member, self.requested_by, self.created_at)


class Member(MemberInfo):
    registration_number = models.IntegerField(null=True, default=None)
    registration_year = models.IntegerField(null=True, default=None)
    sector = models.IntegerField(null=True, default=None)
    branch = models.IntegerField(null=True, default=None)
    rfc = models.CharField(max_length=13, null=True, default=None)
