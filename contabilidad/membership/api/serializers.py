from ..models import MembershipRequest
from rest_framework import serializers


class MembershipRequestSerializer(serializers.ModelSerializer):

    class Meta:
        model = MembershipRequest
        fields = '__all__'
