from rest_framework_nested import routers
from . import views


router = routers.DefaultRouter()
router.register("tickets", views.TicketViewSet)

urlpatterns = router.urls
