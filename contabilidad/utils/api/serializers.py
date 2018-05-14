from rest_framework import serializers
from django.contrib.auth.models import User
from membership.models import Sector, Branch, State, SCIAN, TariffFraction, Region
from membership.api.serializers import StateSerializer, SectorSerializer, BranchSerializer, SCIANSerializer, \
    TariffFractionSerializer, RegionSerializer
from datetime import datetime
from django.conf import settings
from users.api.serializers import *
from ..models import Comment

import pytz

from crum import get_current_user

MONTH_NAMES = {
    1: "enero",
    2: "febrero",
    3: "marzo",
    4: "abril",
    5: "mayo",
    6: "junio",
    7: "julio",
    8: "agosto",
    9: "septiembre",
    10: "octubre",
    11: "noviembre",
    12: "diciembre"
}


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
    branches = serializers.SerializerMethodField()
    scian = serializers.SerializerMethodField()
    tariff_traffic = serializers.SerializerMethodField()
    regions = serializers.SerializerMethodField()

    def get_states(self, obj):
        return StateSerializer(State.objects.all().prefetch_related('municipality', 'municipality__suburb'),
                               many=True).data

    def get_sectors(self, obj):
        return SectorSerializer(Sector.objects.all(), many=True).data

    def get_branches(self, obj):
        return BranchSerializer(Branch.objects.all(), many=True).data

    def get_scian(self, obj):
        return SCIANSerializer(SCIAN.objects.all(), many=True).data

    def get_tariff_traffic(self, obj):
        return TariffFractionSerializer(TariffFraction.objects.all(), many=True).data

    def get_regions(self, obj):
        return RegionSerializer(Region.objects.all(), many=True).data


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.IntegerField(write_only=True, max_value=10000, min_value=1, required=True)
    message = serializers.CharField(max_length=250, write_only=True, required=True, allow_blank=False)
    source = UserSerializer(read_only=True)
    destination = UserSerializer(read_only=True)
    date = serializers.SerializerMethodField(read_only=True)
    source_full_name = serializers.SerializerMethodField(read_only=True)
    destination_full_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Comment
        exclude = ('id',)

    def get_date(self, obj):
        return "{day}/{month}/{year}".format(day=obj.timestamp.day, month=MONTH_NAMES.get(obj.timestamp.month, 'MES'),
                                             year=obj.timestamp.year)

    def get_source_full_name(self, obj):
        return obj.source.get_full_name()

    def get_destination_full_name(self, obj):
        return obj.destination.get_full_name()

    def validate(self, data):
        validated_data = super(CommentSerializer, self).validate(data)
        user_id = validated_data.get('user')

        self.destination_user = User.objects.filter(pk=user_id).first()

        if self.destination_user is None:
            raise serializers.ValidationError("El Usuario no existe")
        return validated_data

    def create(self, validated_data):
        source = get_current_user()
        msg = validated_data.get('message')
        instance = Comment.objects.create(msg=msg, source=source, destination=self.destination_user)
        return instance


class APISerializer(serializers.Serializer):
    creation_timestamp = serializers.SerializerMethodField()

    def get_creation_timestamp(self, obj):
        return settings.API_TIMESTAMP
