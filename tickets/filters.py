import django_filters
from .models import Ticket


class CharInFilter(django_filters.CharFilter, django_filters.BaseInFilter):
    pass


class TicketFilter(django_filters.FilterSet):
    status = CharInFilter(field_name="status", lookup_expr="in")
    priority = CharInFilter(field_name="priority", lookup_expr="in")

    class Meta:
        model = Ticket
        fields = ["status", "priority"]
