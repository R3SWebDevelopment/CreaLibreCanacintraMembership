from ..models import MembershipRequest, SAT_PERSON_TYPE, SAT_ORGANIZATION_TYPE, State, Municipality, Suburb, Sector, \
    Branch, SCIAN, TariffFraction, AttachedFile, Member, Region, RegionDelegation
from rest_framework import serializers


class RegionDelegationSerializer(serializers.ModelSerializer):

    class Meta:
        model = RegionDelegation
        fields = '__all__'


class RegionSerializer(serializers.ModelSerializer):
    delegations = RegionDelegationSerializer(source='delegations.all', many=True)

    class Meta:
        model = Region
        fields = '__all__'


class MembershipRequestAttachment(serializers.ModelSerializer):
    type = serializers.CharField(read_only=True)
    file = serializers.FileField(read_only=True)
    url = serializers.URLField(read_only=True)
    name = serializers.CharField(read_only=True, source="file.name")
    types = serializers.ListField(
        child=serializers.CharField(),
        write_only=True
    )
    files = serializers.ListField(
        child=serializers.FileField(),
        write_only=True
    )

    class Meta:
        model = AttachedFile
        fields = '__all__'

    def create(self, validated_data):
        attachment = []
        for item in zip(validated_data.get('types', []), validated_data.get('files', [])):
            attachment.append(super(MembershipRequestAttachment, self).create({
                "type": item[0],
                "file": item[1]
            }))
        return attachment


class MembershipAttachment(serializers.ModelSerializer):
    type = serializers.CharField(read_only=True)
    file = serializers.FileField(read_only=True)
    url = serializers.URLField(read_only=True)
    name = serializers.CharField(read_only=True, source="file.name")

    class Meta:
        model = AttachedFile
        fields = '__all__'


class MembershipRequestAcceptance(serializers.ModelSerializer):
    membership_request = serializers.IntegerField(write_only=True, required=True)
    promoter_office = serializers.CharField(write_only=True, required=True)
    promoter_name = serializers.CharField(write_only=True, required=True)
    payment_date = serializers.DateField(write_only=True, required=True)
    business_contact = serializers.CharField(write_only=True, required=True)
    membership_feed = serializers.DecimalField(write_only=True, required=True, max_digits=10, decimal_places=2)

    class Meta:
        model = Member
        fields = ('membership_request', 'promoter_office', 'promoter_name', 'payment_date', 'business_contact',
                  'membership_feed')

    def validate(self, data):
        validated_data = super(MembershipRequestAcceptance, self).validate(data)
        if 'membership_request' in validated_data.keys():
            self.request = MembershipRequest.objects.filter(id=data['membership_request']).first()
            if self.request is None:
                raise serializers.ValidationError("La solicitud de registro no existe")
            elif not self.request.is_submitted:
                raise serializers.ValidationError("La solicitud de registro todavia no se puede revisar")
        return validated_data

    def create(self, validated_data):
        data = self.request.pdf_data
        other_representative = data.get('other_representative', [])
        for key in ['other_representative', 'is_company', 'is_person']:
            del data[key]
        del validated_data['membership_request']
        for key in ['ceo', 'legal', 'main']:
            del data['{}_name'.format(key)]
            del data['{}_email'.format(key)]
            del data['{}_phone'.format(key)]
        data.update(validated_data)
        instance = Member.objects.create(**data)
        for attachment in self.request.attachment.all():
            instance.attachment.add(attachment)
        MembershipRequest.objects.filter(pk=self.request.pk).update(hidden=True)
        return instance


class MemberSerializer(serializers.ModelSerializer):
    is_person = serializers.NullBooleanField(read_only=True)
    is_company = serializers.NullBooleanField(read_only=True)
    ceo_name = serializers.CharField(read_only=True)
    ceo_email = serializers.CharField(read_only=True)
    ceo_phone = serializers.CharField(read_only=True)
    legal_name = serializers.CharField(read_only=True)
    legal_email = serializers.CharField(read_only=True)
    legal_phone = serializers.CharField(read_only=True)
    main_name = serializers.CharField(read_only=True)
    main_email = serializers.CharField(read_only=True)
    main_phone = serializers.CharField(read_only=True)
    attachment = MembershipRequestAttachment(many=True, read_only=True)

    class Meta:
        model = Member
        fields = '__all__'


class MembershipRequestSerializer(serializers.ModelSerializer):
    is_submitted = serializers.NullBooleanField(required=False, read_only=True)
    can_edit = serializers.NullBooleanField(required=False, read_only=True)
    has_change_form = serializers.NullBooleanField(required=False, read_only=True)
    can_load_attachment = serializers.NullBooleanField(required=False, read_only=True)
    has_create_pdf = serializers.NullBooleanField(required=False, read_only=True)
    can_download_form = serializers.NullBooleanField(required=False, read_only=True)
    can_submit = serializers.NullBooleanField(required=False, read_only=True)
    is_required_field_fulfilled = serializers.NullBooleanField(required=False, read_only=True)
    form_pdf_url = serializers.URLField(required=False, read_only=True)

    is_person = serializers.NullBooleanField(required=False)
    is_company = serializers.NullBooleanField(required=False)
    ceo_name = serializers.CharField(required=False, allow_blank=True)
    ceo_email = serializers.CharField(required=False, allow_blank=True)
    ceo_phone = serializers.CharField(required=False, allow_blank=True)
    legal_name = serializers.CharField(required=False, allow_blank=True)
    legal_email = serializers.CharField(required=False, allow_blank=True)
    legal_phone = serializers.CharField(required=False, allow_blank=True)
    main_name = serializers.CharField(required=False, allow_blank=True)
    main_email = serializers.CharField(required=False, allow_blank=True)
    main_phone = serializers.CharField(required=False, allow_blank=True)
    attachment = MembershipRequestAttachment(read_only=True, many=True)

    class Meta:
        model = MembershipRequest
        fields = '__all__'

    def validate(self, data):

        is_person = data.get('is_person', None)
        if is_person is not None:
            del data['is_person']
        is_company = data.get('is_company', None)
        if is_company is not None:
            del data['is_company']

        if (is_person and is_company) or (not is_person and not is_company):
            raise serializers.ValidationError("Debe de seleccionar Persona Física o Persona Moral")

        if is_person is not None or is_company is not None:
            data['sat_taxpayer_type'] = SAT_PERSON_TYPE if is_person else SAT_ORGANIZATION_TYPE if is_company else None

        data['ceo'] = {
            'name': data.get('ceo_name', ''),
            'email': data.get('ceo_email', ''),
            'phone': data.get('ceo_phone', ''),
        }
        del data['ceo_name']
        del data['ceo_email']
        del data['ceo_phone']

        data['legal_representative'] = {
            'name': data.get('legal_name', ''),
            'email': data.get('legal_email', ''),
            'phone': data.get('legal_phone', ''),
        }
        del data['legal_name']
        del data['legal_email']
        del data['legal_phone']

        data['main_representative'] = {
            'name': data.get('main_name', ''),
            'email': data.get('main_email', ''),
            'phone': data.get('main_phone', ''),
        }
        del data['main_name']
        del data['main_email']
        del data['main_phone']

        return data

    def update(self, instance, validated_data):
        return super(MembershipRequestSerializer, self).update(instance, validated_data)


class MembershipRequestPdfSerializer(MembershipRequestSerializer):
    class Meta:
        model = MembershipRequest
        exclude = ('attachment', 'id', 'created_at', 'requested_at', 'validated', 'requested_by', 'attended_by',
                   'member', 'pdf_data', 'is_submitted', 'can_edit', 'has_change_form', 'can_load_attachment',
                   'has_create_pdf', 'can_download_form', 'can_submit', 'is_required_field_fulfilled', 'form_pdf_url')


class SuburbSerializer(serializers.ModelSerializer):
    state = serializers.CharField(source='municipality.state.name')
    municipality = serializers.CharField(source='municipality.name')
    municipalities = serializers.ListField(source='municipalities_name')
    suburbs = serializers.ListField(source='suburbs_name')
    suburb = serializers.CharField(source='suburb_name')

    class Meta:
        model = Suburb
        fields = '__all__'


class SuburbSimpleSerializer(serializers.ModelSerializer):
    state = serializers.CharField(source='municipality.state.name')
    municipalities = serializers.ListField(source='municipalities_name')

    class Meta:
        model = Suburb
        fields = ('state', 'municipalities', )


class SuburbMunicipalitySerializer(serializers.ModelSerializer):
    state = serializers.CharField(source='municipality.state.name')
    municipality = serializers.CharField(source='municipality.name')
    municipalities = serializers.ListField(source='municipalities_name')
    suburbs = serializers.ListField(source='municipality.suburbs_name')

    class Meta:
        model = Suburb
        fields = ('state', 'municipalities', 'municipality', 'suburbs', )


class SuburbWithoutZipCodeSerializer(serializers.ModelSerializer):
    state = serializers.CharField(source='municipality.state.name')
    municipality = serializers.CharField(source='municipality.name')
    municipalities = serializers.ListField(source='municipalities_name')
    suburbs = serializers.ListField(source='municipality.suburbs_name')
    suburb = serializers.CharField(source='name')

    class Meta:
        model = Suburb
        fields = ('state', 'municipalities', 'municipality', 'suburbs', 'suburb', 'zip_code')


class StateSerializer(serializers.ModelSerializer):

    class Meta:
        model = State
        fields = ('name', )


class BranchSerializer(serializers.ModelSerializer):

    class Meta:
        model = Branch
        fields = '__all__'


class SectorSerializer(serializers.ModelSerializer):
    branches = BranchSerializer(many=True, source='branches.all')

    class Meta:
        model = Sector
        fields = '__all__'


class SCIANSerializer(serializers.ModelSerializer):

    class Meta:
        model = SCIAN
        fields = '__all__'


class TariffFractionSerializer(serializers.ModelSerializer):

    class Meta:
        model = TariffFraction
        fields = '__all__'
