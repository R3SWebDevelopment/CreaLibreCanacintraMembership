from rest_framework import serializers
from rest_framework import fields
from ..models import Company
from utils.api.serializers import UserSerializer
from membership.api.serializers import MemberSerializer, MembershipRequestSerializer
from django.contrib.auth.models import User


class CompanySerializer(serializers.ModelSerializer):
    collaborators = UserSerializer(many=True, read_only=True)
    is_member = serializers.BooleanField(read_only=True)
    has_membership_request = serializers.BooleanField(read_only=True)
    membership = MemberSerializer(read_only=True)
    membership_request = MembershipRequestSerializer(read_only=True)

    class Meta:
        model = Company
        fields = ('full_name', 'rfc', 'address', 'collaborators', 'is_member', 'has_membership_request', 'membership',
                  'membership_request')


class AddCollaboratorsSerializer(serializers.Serializer):
    users = fields.ListField(fields.IntegerField)

    def get_users(self):
        return User.objects.filter(pk__in=self.data.get('users', []))
