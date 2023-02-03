from rest_framework import serializers
from .models import Ticket, TicketType
from authentication.serializers import UserSerializer
from projects.serializers import ProjectReadSnippetSerializer


class TicketTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketType
        fields = ["id", "title"]


class TicketTypeWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketType
        fields = ["title", "project"]


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
            "project",
            "assigned_to",
            "created_by",
        ]

    type = TicketTypeSerializer()
    assigned_to = UserSerializer()
    created_by = UserSerializer()
    project = ProjectReadSnippetSerializer()


class TicketWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ["title", "description", "type", "project", "assigned_to"]
