from rest_framework import serializers
from .models import Ticket, TicketType
from authentication.serializers import UserSerializer


class TicketTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketType
        fields = ["id", "title"]


class TicketReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = [
            "id",
            "title",
            "description",
            "created_at",
            "updated_at",
            "type",
            "assigned_to",
            "created_by",
        ]

    type = TicketTypeSerializer()
    assigned_to = UserSerializer()
    created_by = UserSerializer()


class TicketWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ["title", "description", "type", "assigned_to"]
