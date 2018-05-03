from rest_framework import serializers
from rest_framework import fields
from ..models import Company, ProductService, Certification
from utils.api.serializers import UserSerializer
from membership.api.serializers import MemberSerializer, MembershipRequestSerializer
from django.contrib.auth.models import User


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

    class Meta:
        model = Company
        fields = ('full_name', 'rfc', 'address', 'collaborators', 'is_member', 'has_membership_request', 'membership',
                  'membership_request', 'can_request_membership', 'can_request_update', 'has_update_membership_request',
                  'can_renew', 'has_payment')


class AddCollaboratorsSerializer(serializers.Serializer):
    users = fields.ListField(fields.IntegerField)

    def get_users(self):
        return User.objects.filter(pk__in=self.data.get('users', []))


class ProductServiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductService
        fields = '__all__'


class CertificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certification
        fields = '__all__'
