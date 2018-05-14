# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.postgres.fields.jsonb import JSONField as JSONBField
from django.contrib.postgres.fields import ArrayField, JSONField
from django.contrib.auth.models import User
from django.utils.functional import cached_property
from django.urls import reverse
from utils.models import HiddenModelManager
import datetime
import re

SAT_PERSON_TYPE = 1
SAT_ORGANIZATION_TYPE = 2
SAT_TAXPAYER_TYPE = (
    (SAT_PERSON_TYPE, "Física"),
    (SAT_ORGANIZATION_TYPE, "Moral")
)

SAT_TAXPAYER_TYPES = [
    SAT_PERSON_TYPE,
    SAT_ORGANIZATION_TYPE
]

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
MEMBERSHIP_REQUEST_FORM = 'MEMBERSHIP_REQUEST_FORM'

SAT_PERSON_TYPE_ATTACHMENT = [
    OFFICIAL_ID,
    REGISTRATION_REGISTER,
    LAST_EMPLOYERS_FEED,
    LAST_TAX_RETURN,
    RFC,
    MEMBERSHIP_REQUEST_FORM
]

SAT_ORGANIZATION_TYPE_ATTACHMENT = [
    CONSTITUTIVE_ACT,
    LEGAL_POWER,
    EMPLOYERS_FEED,
    LEGAL_REPRESENTATIVE_OFFICIAL_ID,
    LAST_TAX_RETURN,
    RFC,
    MEMBERSHIP_REQUEST_FORM
]

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
    (MEMBERSHIP_REQUEST_FORM, "Solicitud de Afiliación impresa firmada por representante legal")
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
    rfc = models.CharField(max_length=13, null=True, default=None)
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
    phone = models.CharField(max_length=250, null=True, default=None)
    mobile = models.CharField(max_length=14, null=True, default=None)
    main_activity_description = models.CharField(max_length=250, null=True, default=None)
    scian_code = models.CharField(max_length=250, null=True, default=None)
    main_product_service = models.CharField(max_length=250, null=True, default=None)
    tariff_fraction = models.CharField(max_length=250, null=True, default=None)
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
    ceo = JSONField(null=True)
    legal_representative = JSONField(null=True)
    main_representative = JSONField(null=True)
    # other representative have the same format as the CEO, legal representative and main representative plus additional
    # fields
    # {
    #   "area_name": "AAAAAA AAAAA AAAAA"
    # }
    other_representative = JSONField(null=True)
    website = models.CharField(max_length=250, null=True, default=None)

    class Meta:
        abstract = True

    @property
    def ceo_name(self):
        return self.ceo.get('name', '') if self.ceo is not None else ''

    @property
    def ceo_email(self):
        return self.ceo.get('email', '') if self.ceo is not None else ''

    @property
    def ceo_phone(self):
        return self.ceo.get('phone', '') if self.ceo is not None else ''

    @property
    def legal_name(self):
        return self.legal_representative.get('name', '') if self.legal_representative is not None else ''

    @property
    def legal_email(self):
        return self.legal_representative.get('email', '') if self.legal_representative is not None else ''

    @property
    def legal_phone(self):
        return self.legal_representative.get('phone', '') if self.legal_representative is not None else ''

    @property
    def main_name(self):
        return self.main_representative.get('name', '') if self.main_representative is not None else ''

    @property
    def main_email(self):
        return self.main_representative.get('email', '') if self.main_representative is not None else ''

    @property
    def main_phone(self):
        return self.main_representative.get('phone', '') if self.main_representative is not None else ''

    def __figure_sat_taxpayer_type(self):
        if self.rfc:
            is_person_pattern = re.compile(r"[A-Z]{4}[0-9]{6}[A-Z0-9]{3}", re.I)
            is_company_pattern = re.compile(r"[A-Z]{3}[0-9]{6}[A-Z0-9]{3}", re.I)
            if is_person_pattern.match(self.rfc) is not None:
                self.sat_taxpayer_type = SAT_PERSON_TYPE
                self.save()
            elif is_company_pattern.match(self.rfc) is not None:
                self.sat_taxpayer_type = SAT_ORGANIZATION_TYPE
                self.save()

    @property
    def is_person(self):
        if self.sat_taxpayer_type is None:
            self.__figure_sat_taxpayer_type()
        return self.sat_taxpayer_type == SAT_PERSON_TYPE

    @property
    def is_company(self):
        if self.sat_taxpayer_type is None:
            self.__figure_sat_taxpayer_type()
        return self.sat_taxpayer_type == SAT_ORGANIZATION_TYPE

    @property
    def required_fields(self):
        return REQUIRED_FILES.get(int(self.sat_taxpayer_type)) if self.sat_taxpayer_type is not None else []

    def setAddress(self, street_name_1=None, street_number=None, apartment_number=None, suburb=None, zip_code=None,
                   municipality=None, state=None):
        self.street_name_1 = street_name_1
        self.street_number = street_number
        self.apartment_number = apartment_number
        self.suburb = suburb
        self.zip_code = zip_code
        self.municipality = municipality
        self.state = state


class AttachedFile(models.Model):
    type = models.CharField(max_length=100, choices=FILE_TYPE_CHOICES)
    file = models.FileField(upload_to="attachment")

    def __str__(self):
        label = get_file_type_label(self.type)
        return "{} - {}".format(label if label is not None else self.type, self.file.name)

    @property
    def url(self):
        return reverse('membership_request:membership_request_attachment_view', kwargs={
            "id": self.id
        })


class MembershipRequest(MemberInfo):
    registration_number = models.IntegerField(null=True, default=None)
    registration_year = models.IntegerField(null=True, default=None)
    sector = models.CharField(max_length=250, null=True, default=None)
    branch = models.CharField(max_length=250, null=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    requested_by = models.ForeignKey(User, related_name="membership_requests", null=True)
    requested_at = models.DateTimeField(null=True, default=None)
    attended_by = models.ForeignKey(User, related_name="membership_requests_approved", null=True)
    validated = models.NullBooleanField(null=True, default=None)
    member = models.OneToOneField("Member", related_name="request", null=True)
    attachment = models.ManyToManyField(AttachedFile)
    pdf_data = JSONField(null=True)
    hidden = models.NullBooleanField(default=False)

    objects = HiddenModelManager()

    required_fields = [
        'registration_year',
        'registration_number',
        'sector',
        'branch',
        'sat_taxpayer_type',
        'rfc',
        'business_name',
        'trade_name',
        'street_name_1',
        'street_number',
        'suburb',
        'zip_code',
        'municipality',
        'state',
        'phone',
        'mobile',
        'main_activity_description',
        'scian_code',
        'main_product_service',
        'tariff_fraction',
        'begins_operations',
        'total_employees',
        'gross_sell_range',
        'website'
    ]

    @property
    def is_submitted(self):
        if self.requested_by is not None and self.requested_at is not None:
            return True
        return False

    @property
    def can_edit(self):
        return False if self.is_submitted else True

    @property
    def has_change_form(self):
        if self.has_create_pdf:
            return not self.pdf_data == self.pdf_context
        return False

    @property
    def can_load_attachment(self):
        if self.is_required_field_fulfilled and self.has_create_pdf and not self.has_change_form \
                and not self.is_submitted:
            return True
        return False

    @property
    def has_create_pdf(self):
        return True if self.pdf_data is not None else False

    @property
    def can_download_form(self):
        return self.is_required_field_fulfilled and not self.is_submitted

    @property
    def can_submit(self):
        if not self.is_submitted:
            if self.is_required_field_fulfilled and self.attachment_fulfill:
                return True
        return False

    @property
    def generate_pdf_data(self):
        from .api.serializers import MembershipRequestPdfSerializer
        try:
            return MembershipRequestPdfSerializer(self).data
        except Exception as e:
            return None

    @property
    def pdf_context(self):
        self.pdf_data = self.generate_pdf_data
        self.save()
        return self.pdf_data

    @property
    def is_required_field_fulfilled(self):
        data = self.generate_pdf_data
        for field in self.__class__.required_fields:
            value = data.get(field, None)
            if value is None:
                return False
        return True

    @property
    def attachment_fulfill(self):
        attachments = SAT_ORGANIZATION_TYPE_ATTACHMENT if self.sat_taxpayer_type == SAT_ORGANIZATION_TYPE \
            else SAT_PERSON_TYPE_ATTACHMENT if self.sat_taxpayer_type == SAT_PERSON_TYPE else []
        for attachment in attachments:
            if self.attachment.filter(type__iexact=attachment) is None:
                return False
        return True

    @property
    def form_pdf_url(self):
        return "{}?id={}".format(reverse('membership_request:generate_membership_request'), self.id)

    @property
    def submit_errors(self):
        data = {
            'error': 'No puede enviar su formulario'
        }
        return data

    def do_submit(self, user=None):
        if self.can_submit:
            self.requested_by = user
            self.requested_at = datetime.datetime.now()
            self.save()

    def add_attachment(self, attachment):
        if self.sat_taxpayer_type is None or self.sat_taxpayer_type not in SAT_TAXPAYER_TYPES:
            raise Exception('El tipo de contribuyente no se ha definido correctamente', 'general')
        if self.sat_taxpayer_type == SAT_PERSON_TYPE:  # The tax payer is a person
            if attachment.type not in SAT_PERSON_TYPE_ATTACHMENT:
                raise Exception('Este archivo no es permitido para una persona física', attachment.type)
        elif self.sat_taxpayer_type == SAT_ORGANIZATION_TYPE:  # The tax payer is an organization
            if attachment.type not in SAT_ORGANIZATION_TYPE_ATTACHMENT:
                raise Exception('Este archivo no es permitido para una persona moral', attachment.type)

        existing = self.attachment.filter(type=attachment.type).first()
        if existing:
            self.attachment.remove(existing)
        self.attachment.add(attachment)

    def __str__(self):
        return "{} - {}".format(self.requested_by, self.created_at)


class UpdateRequest(MemberInfo):
    member = models.OneToOneField("Member", related_name="update_requests")
    created_at = models.DateTimeField(auto_now_add=True)
    requested_by = models.ForeignKey(User, related_name="update_requests", null=True)
    requested_at = models.DateTimeField(null=True, default=None)
    attended_by = models.ForeignKey(User, related_name="update_requests_approved", null=True)
    validated = models.NullBooleanField(null=True, default=None)
    hidden = models.NullBooleanField(default=False)

    objects = HiddenModelManager()

    def __str__(self):
        return "{} - {} - {}".format(self.member, self.requested_by, self.created_at)


class Member(MemberInfo):
    registration_number = models.IntegerField(null=True, default=None)
    registration_year = models.IntegerField(null=True, default=None)
    sector = models.CharField(max_length=250, null=True, default=None)
    branch = models.CharField(max_length=250, null=True, default=None)
    promoter_office = models.CharField(max_length=250, null=True, default=None)
    promoter_name = models.CharField(max_length=250, null=True, default=None)
    payment_date = models.DateField(null=True, default=None)
    business_contact = models.CharField(max_length=250, null=True, default=None)
    membership_feed = models.DecimalField(null=True, default=None, max_digits=12, decimal_places=2)
    allowed_person = models.ManyToManyField(User, related_name="members")
    attachment = models.ManyToManyField(AttachedFile)
    hidden = models.NullBooleanField(default=False)

    objects = HiddenModelManager()

    def __str__(self):
        return "{}".format(self.rfc)


class State(models.Model):
    name = models.CharField(max_length=250)
    zip_codes = ArrayField(
        models.CharField(max_length=5, blank=True),
        null=True,
        default=None
    )
    municipalities = JSONBField(default=list, null=True, blank=True)

    class Meta:
        ordering = ('name', )

    def __str__(self):
        return "{}".format(self.name)


class Municipality(models.Model):
    state = models.ForeignKey(State, related_name="municipality")
    name = models.CharField(max_length=250)

    class Meta:
        ordering = ('state', 'name')

    def __str__(self):
        return "{} - {}".format(self.state, self.name)

    @cached_property
    def suburbs(self):
        return self.suburb.all()

    @cached_property
    def zip_codes(self):
        return self.suburbs.values_list('zip_code', flat=True).order_by('zip_code').distinct()

    @property
    def suburbs_name(self):
        return list(self.suburbs.values_list('name', flat=True).order_by('name').distinct())


class Suburb(models.Model):
    municipality = models.ForeignKey(Municipality, related_name="suburb")
    name = models.CharField(max_length=250)
    zip_code = models.CharField(max_length=5)

    class Meta:
        ordering = ('municipality', 'name')

    def __str__(self):
        return "{} - {} ({})".format(self.municipality, self.name, self.zip_code)

    @cached_property
    def siblings(self):
        return self.__class__.objects.filter(zip_code=self.zip_code)

    @property
    def suburbs_name(self):
        return self.siblings.values_list('name', flat=True).\
            order_by('name').distinct()

    @property
    def suburb_name(self):
        suburbs = self.siblings
        if len(suburbs) == 0:
            return self.name
        return ""

    @property
    def municipalities_name(self):
        return list(self.municipality.state.municipality.all().values_list('name', flat=True).order_by('name')
                    .distinct())

    @property
    def municipality_name(self):
        self.municipality


class Sector(models.Model):
    code = models.CharField(max_length=3, null=False)
    description = models.CharField(max_length=250, null=False)

    class Meta:
        ordering = ('code', 'description')

    def __str__(self):
        return "{} - {}".format(self.code, self.description)


class Branch(models.Model):
    sector = models.ForeignKey(Sector, null=False, related_name='branches')
    code = models.CharField(max_length=10, null=False)
    description = models.CharField(max_length=250, null=False)

    class Meta:
        ordering = ('sector', 'code', 'description')

    def __str__(self):
        return "{}: {} - {}".format(self.sector, self.code, self.description)


class SCIAN(models.Model):
    code = models.CharField(max_length=10, null=False)
    description = models.CharField(max_length=250, null=False)

    class Meta:
        ordering = ('code', 'description')

    def __str__(self):
        return "{} - {}".format(self.code, self.description)


class TariffFraction(models.Model):
    code = models.CharField(max_length=10, null=False)
    description = models.TextField(null=False)

    class Meta:
        ordering = ('code', 'description')

    def __str__(self):
        return "{} - {}".format(self.code, self.description)


class Region(models.Model):
    code = models.CharField(max_length=10, null=False)
    description = models.CharField(max_length=250, null=False)

    class Meta:
        ordering = ('code', 'description')

    def __str__(self):
        return "{} - {}".format(self.code, self.description)


class RegionDelegation(models.Model):
    region = models.ForeignKey(Region, related_name="delegations")
    code = models.CharField(max_length=10, null=False)
    description = models.CharField(max_length=250, null=False)

    class Meta:
        ordering = ('code', 'description')

    def __str__(self):
        return "{} - {} - {}".format(self.region, self.code, self.description)
