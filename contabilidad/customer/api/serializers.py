from rest_framework import serializers
from rest_framework import fields
from ..models import Company
from utils.api.serializers import UserSerializer
from django.contrib.auth.models import User


class CompanySerializer(serializers.ModelSerializer):
    collaborators = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Company
        fields = ('full_name', 'rfc', 'address', 'collaborators')


class AddCollaboratorsSerializer(serializers.Serializer):
    users = fields.ListField(fields.IntegerField)

    def get_users(self):
        return User.objects.filter(pk__in=self.data.get('users', []))
