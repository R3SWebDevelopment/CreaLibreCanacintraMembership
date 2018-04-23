from rest_framework import serializers
from django.contrib.auth.models import User
from membership.models import Sector, State
from membership.api.serializers import StateSerializer, SectorSerializer
from datetime import datetime
from django.conf import settings
import pytz


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'


class HealthCheckSerializer(serializers.Serializer):
    timestamp = serializers.SerializerMethodField()
    image = serializers.URLField(read_only=True,
                                 default="http://via.placeholder.com/800x600/000000/ffffff/?text=Place%20Holder")
    message = serializers.SerializerMethodField()
    maintenance = serializers.BooleanField(default=False)

    def get_message(self, obj):
        return "test"

    def get_timestamp(self, obj):
        return datetime.now(pytz.timezone(settings.TIME_ZONE)).strftime("%Y-%m-%dT%H:%M:%S%Z")


class CatalogSerializer(serializers.Serializer):
    states = serializers.SerializerMethodField()
    sectors = serializers.SerializerMethodField()

    def get_states(self, obj):
        return StateSerializer(State.objects.all(), many=True).data

    def get_sectors(self, obj):
        return SectorSerializer(Sector.objects.all(), many=True).data
