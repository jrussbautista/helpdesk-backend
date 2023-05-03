from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST
from drf_rw_serializers.viewsets import ModelViewSet
from .filters import TicketFilter
from .pagination import DefaultPagination


from .models import Ticket, TicketType
from .serializers import (
    TicketReadSerializer,
    TicketWriteSerializer,
    TicketTypeSerializer,
    TicketTypeWriteSerializer,
)
from .permissions import IsTicketOwner
from .constants import TicketStatus


class TicketViewSet(ModelViewSet):
    queryset = Ticket.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = TicketReadSerializer
    write_serializer_class = TicketWriteSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_class = TicketFilter
    pagination_class = DefaultPagination
    ordering_fields = ["created_at", "updated_at"]
    ordering = ["created_at"]
    search_fields = ["title", "description"]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(
        detail=True,
        methods=["post"],
        permission_classes=[IsAdminUser | IsTicketOwner],
        url_path="processing",
    )
    def processing(self, request, pk=None):
        ticket = self.get_object()
        if ticket.status in [TicketStatus.CANCELLED, TicketStatus.RESOLVED]:
            return Response(status=HTTP_400_BAD_REQUEST)
        ticket.processing()
        serializer = self.serializer_class(ticket)
        return Response(serializer.data)

    @action(
        detail=True,
        methods=["post"],
        permission_classes=[IsAdminUser | IsTicketOwner],
        url_path="resolved",
    )
    def resolved(self, request, pk=None):
        ticket = self.get_object()
        if ticket.status in [TicketStatus.CANCELLED]:
            return Response(status=HTTP_400_BAD_REQUEST)
        ticket.resolved()
        serializer = self.serializer_class(ticket)
        return Response(serializer.data)

    @action(
        detail=True,
        methods=["post"],
        permission_classes=[IsAdminUser | IsTicketOwner],
        url_path="cancel",
    )
    def cancel(self, request, pk=None):
        ticket = self.get_object()
        if ticket.status in [TicketStatus.PROCESSING, TicketStatus.RESOLVED]:
            return Response(status=HTTP_400_BAD_REQUEST)
        ticket.cancel()
        serializer = self.serializer_class(ticket)
        return Response(serializer.data)


class TicketTypeViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = TicketTypeSerializer
    write_serializer_class = TicketTypeWriteSerializer

    def get_queryset(self):
        project_id = self.request.GET.get("project_id")
        if project_id:
            return TicketType.objects.filter(project_id=project_id)
        return None
