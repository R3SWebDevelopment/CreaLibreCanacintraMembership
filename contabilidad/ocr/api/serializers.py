from rest_framework import serializers
from ..models import OCRRequest
from utils.api.serializers import UserSerializer


class OCRRequestSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    updated_by = UserSerializer(read_only=True)
    working_path = serializers.CharField(read_only=True)
    result = serializers.CharField(read_only=True)
    log = serializers.JSONField(read_only=True)

    class Meta:
        model = OCRRequest
        fields = '__all__'
