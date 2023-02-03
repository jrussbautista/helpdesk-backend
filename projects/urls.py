from rest_framework_nested import routers
from . import views


router = routers.DefaultRouter()
router.register("projects", views.ProjectViewSet, basename="projects")

urlpatterns = router.urls
