from ..models import MembershipRequest
from rest_framework import serializers
from rest_auth.registration.serializers import RegisterSerializer

class MembershipRequestSerializer(RegisterSerializer):

    class Meta:
        model = MembershipRequest
        fields = '__all__'