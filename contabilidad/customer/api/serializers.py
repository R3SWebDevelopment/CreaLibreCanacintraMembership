from rest_framework import serializers
from rest_framework import fields
from ..models import Company, ProductService, Certification
from utils.api.serializers import UserSerializer
from membership.api.serializers import MemberSerializer, MembershipRequestSerializer
from django.contrib.auth.models import User
from crum import get_current_user


class ProductServiceSerializer(serializers.ModelSerializer):
    selected = serializers.ListField(child=serializers.IntegerField(), write_only=True, required=True)

    def validate_selected(self, value):
        qs = ProductService.objects.filter(pk__in=value)
        if qs.count() != len(set(value)):
            raise serializers.ValidationError("Uno de los productos o servicios no estan registrados")
        return qs

    class Meta:
        model = ProductService
        fields = '__all__'
        read_only_fields = ('code', 'name')


class CertificationSerializerWrite(serializers.ModelSerializer):

    class Meta:
        model = Certification
        fields = ('name', 'file')

    def create(self, validated_data):
        print("write validated_data: {}".format(validated_data))
        return [1, 2]


class CertificationSerializer(serializers.ModelSerializer):
    is_public = serializers.BooleanField(write_only=True, required=True)
    url = serializers.URLField(read_only=True)
    names = serializers.ListField(
        child=serializers.CharField(),
        write_only=True
    )
    files = serializers.ListField(
        child=serializers.FileField(),
        write_only=True
    )

    class Meta:
        model = Certification
        fields = '__all__'
        read_only_fields = ('code', 'name', 'id')

    def create(self, validated_data):
        user = get_current_user()
        if user is not None and user.profile is not None:
            company = user.profile.my_company
            if company is not None:
                company.certification_is_public = validated_data.get('is_public', False)
                company.save()
                for item in zip(validated_data.get('names', []), validated_data.get('files', [])):
                    Certification.objects.create(company=company, name=item[0], file=item[1])
        return []


class CompanySerializer(serializers.ModelSerializer):
    collaborators = UserSerializer(many=True, read_only=True)
    is_member = serializers.BooleanField(read_only=True)
    has_membership_request = serializers.BooleanField(read_only=True)
    membership = MemberSerializer(read_only=True)
    membership_request = MembershipRequestSerializer(read_only=True)
    can_request_membership = serializers.BooleanField(read_only=True)
    can_request_update = serializers.BooleanField(read_only=True)
    has_update_membership_request = serializers.BooleanField(read_only=True)
    can_renew = serializers.BooleanField(read_only=True)
    has_payment = serializers.BooleanField(read_only=True)
    product_services = ProductServiceSerializer(read_only=True, many=True)
    certifications = CertificationSerializer(read_only=True, many=True)
    product_services_id = serializers.ListField(write_only=True, required=False,
                                                child=serializers.IntegerField(min_value=0, max_value=100)
                                                )
    certifications_id = serializers.ListField(write_only=True, required=False,
                                              child=serializers.IntegerField(min_value=0, max_value=100)
                                              )
    delegation = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Company
        fields = ('full_name', 'rfc', 'address', 'collaborators', 'is_member', 'has_membership_request', 'membership',
                  'membership_request', 'can_request_membership', 'can_request_update', 'has_update_membership_request',
                  'can_renew', 'has_payment', 'product_services', 'certifications', 'product_services_id',
                  'certifications_id', 'membership_status', 'branch_office', 'state', 'delegation')

    def get_delegation(self, obj):
        return obj.get_delegation


class AddCollaboratorsSerializer(serializers.Serializer):
    users = fields.ListField(fields.IntegerField)

    def get_users(self):
        return User.objects.filter(pk__in=self.data.get('users', []))
