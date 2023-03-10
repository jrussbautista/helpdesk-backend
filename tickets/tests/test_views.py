from rest_framework import status
import pytest
from tickets.factories import TicketFactory
from tickets.constants import TicketStatus


@pytest.fixture
def resolved_ticket(api_client):
    def do_resolved_ticket(id):
        return api_client.post(f"/tickets/{id}/resolved/")

    return do_resolved_ticket


@pytest.fixture
def cancel_ticket(api_client):
    def do_cancel_ticket(id):
        return api_client.post(f"/tickets/{id}/cancel/")

    return do_cancel_ticket


@pytest.mark.django_db
class TestMarkTicketAsResolved:
    def test_logged_in_user_can_mark_ticket_as_resolved(
        self, authenticate, resolved_ticket
    ):
        user = authenticate()
        ticket = TicketFactory(created_by=user)
        response = resolved_ticket(ticket.id)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["status"] == TicketStatus.RESOLVED

    def test_cancelled_ticket_cannot_mark_ticket_as_resolved(
        self, authenticate, resolved_ticket
    ):
        user = authenticate()
        ticket = TicketFactory(created_by=user, status=TicketStatus.CANCELLED)
        response = resolved_ticket(ticket.id)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_user_cannot_mark_other_ticket_as_resolved(
        self, authenticate, resolved_ticket
    ):
        authenticate()
        ticket_by_other = TicketFactory()
        response = resolved_ticket(ticket_by_other.id)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_anonymous_user_cannot_mark_ticket_as_resolved(self, resolved_ticket):
        ticket = TicketFactory()
        response = resolved_ticket(ticket.id)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestMarkTicketAsCancelled:
    def test_logged_in_user_can_mark_ticket_as_cancelled(
        self, authenticate, cancel_ticket
    ):
        user = authenticate()
        ticket = TicketFactory(created_by=user)
        response = cancel_ticket(ticket.id)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["status"] == TicketStatus.CANCELLED

    def test_in_progress_ticket_cannot_mark_ticket_as_cancelled(
        self, authenticate, cancel_ticket
    ):
        user = authenticate()
        ticket = TicketFactory(created_by=user, status=TicketStatus.IN_PROGRESS)
        response = cancel_ticket(ticket.id)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_resolved_ticket_cannot_mark_ticket_as_cancelled(
        self, authenticate, cancel_ticket
    ):
        user = authenticate()
        ticket = TicketFactory(created_by=user, status=TicketStatus.RESOLVED)
        response = cancel_ticket(ticket.id)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_user_cannot_mark_other_ticket_as_cancelled(
        self, authenticate, cancel_ticket
    ):
        authenticate()
        ticket_by_other = TicketFactory()
        response = cancel_ticket(ticket_by_other.id)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_anonymous_user_cannot_mark_ticket_as_cancelled(self, cancel_ticket):
        ticket = TicketFactory()
        response = cancel_ticket(ticket.id)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
