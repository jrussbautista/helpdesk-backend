from rest_framework_nested import routers
from . import views


router = routers.DefaultRouter()
router.register("tickets", views.TicketViewSet, basename="tickets")
router.register("ticket-types", views.TicketTypeViewSet, basename="ticket-types")

urlpatterns = router.urls
