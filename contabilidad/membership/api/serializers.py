from ..models import MembershipRequest, SAT_PERSON_TYPE, SAT_ORGANIZATION_TYPE, State, Municipality, Sector, Branch, \
    SCIAN, TariffFraction
from rest_framework import serializers


class MembershipRequestSerializer(serializers.ModelSerializer):
    is_person = serializers.NullBooleanField(required=False)
    is_company = serializers.NullBooleanField(required=False)

    class Meta:
        model = MembershipRequest
        exclude = ('attachment',)

    def validate(self, data):
        print(data)

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

        return data

    def update(self, instance, validated_data):
        return super(MembershipRequestSerializer, self).update(instance, validated_data)


class MunicipalitySerializer(serializers.ModelSerializer):

    class Meta:
        model = Municipality
        fields = '__all__'


class StateSerializer(serializers.ModelSerializer):
    municipality = MunicipalitySerializer(many=True, source='municipality.all')

    class Meta:
        model = State
        fields = '__all__'


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
