from .models import Ticket
from .serializers import TicketReadSerializer, TicketWriteSerializer
from rest_framework.permissions import IsAuthenticated
from drf_rw_serializers.viewsets import ModelViewSet


class TicketViewSet(ModelViewSet):
    queryset = Ticket.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = TicketReadSerializer
    write_serializer_class = TicketWriteSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
