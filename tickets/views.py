from .models import Ticket, TicketType
from .serializers import (
    TicketReadSerializer,
    TicketWriteSerializer,
    TicketTypeSerializer,
    TicketTypeWriteSerializer,
)
from rest_framework.permissions import IsAuthenticated
from drf_rw_serializers.viewsets import ModelViewSet


class TicketViewSet(ModelViewSet):
    queryset = Ticket.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = TicketReadSerializer
    write_serializer_class = TicketWriteSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class TicketTypeViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = TicketTypeSerializer
    write_serializer_class = TicketTypeWriteSerializer

    def get_queryset(self):
        project_id = self.request.GET.get("project_id")
        if project_id:
            return TicketType.objects.filter(project_id=project_id)
        return None
