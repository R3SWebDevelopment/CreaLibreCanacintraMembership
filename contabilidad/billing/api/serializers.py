from rest_framework import serializers
from rest_framework import fields
from ..models import Store, Ticket, TicketImage


class StoreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Store
        fields = ('name', )


class TicketImageSerializer(serializers.ModelSerializer):
    image = fields.ImageField(read_only=True)

    class Meta:
        model = TicketImage
        fields = ('image',)


class TicketSerializer(serializers.ModelSerializer):
    log = fields.ListField(child=fields.JSONField())
    info = fields.SerializerMethodField(read_only=True)

    class Meta:
        model = Ticket
        fields = ('store', 'created_at', 'updated_at', 'created_by', 'updated_by', 'is_invoiced', 'log', 'info')

    def get_info(self, obj):
        return {}