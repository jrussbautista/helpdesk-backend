from .models import Project
from .serializers import ProjectReadSerializer, ProjectWriteSerializer
from rest_framework.permissions import IsAuthenticated
from drf_rw_serializers.viewsets import ModelViewSet


class ProjectViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ProjectReadSerializer
    write_serializer_class = ProjectWriteSerializer

    def get_queryset(self):
        owner = self.request.user
        return Project.objects.filter(owner=owner)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
