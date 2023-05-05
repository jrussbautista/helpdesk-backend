from rest_framework import status
import pytest
from tickets.factories import TicketFactory
from tickets.constants import TicketStatus, TicketPriority
from projects.factories import ProjectFactory


@pytest.fixture
def get_tickets(api_client):
    def do_get_tickets(params=""):
        return api_client.get(f"/tickets/?{params}")

    return do_get_tickets


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


@pytest.fixture
def processing_ticket(api_client):
    def do_processing_ticket(id):
        return api_client.post(f"/tickets/{id}/processing/")

    return do_processing_ticket


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

    def test_processing_ticket_cannot_mark_ticket_as_cancelled(
        self, authenticate, cancel_ticket
    ):
        user = authenticate()
        ticket = TicketFactory(created_by=user, status=TicketStatus.PROCESSING)
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


@pytest.mark.django_db
class TestMarkTicketAsProcessing:
    def test_logged_in_user_can_mark_ticket_as_processing(
        self, authenticate, processing_ticket
    ):
        user = authenticate()
        ticket = TicketFactory(created_by=user)
        response = processing_ticket(ticket.id)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["status"] == TicketStatus.PROCESSING

    def test_cancelled_ticket_cannot_mark_ticket_as_processing(
        self, authenticate, processing_ticket
    ):
        user = authenticate()
        ticket = TicketFactory(created_by=user, status=TicketStatus.CANCELLED)
        response = processing_ticket(ticket.id)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_resolved_ticket_cannot_mark_ticket_as_processing(
        self, authenticate, processing_ticket
    ):
        user = authenticate()
        ticket = TicketFactory(created_by=user, status=TicketStatus.RESOLVED)
        response = processing_ticket(ticket.id)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_user_cannot_mark_other_ticket_as_processing(
        self, authenticate, processing_ticket
    ):
        authenticate()
        ticket_by_other = TicketFactory()
        response = processing_ticket(ticket_by_other.id)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_anonymous_user_cannot_mark_ticket_as_processing(self, processing_ticket):
        ticket = TicketFactory()
        response = processing_ticket(ticket.id)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestFilterTickets:
    def test_filter_tickets_by_status(self, authenticate, get_tickets):
        user = authenticate()
        TicketFactory(created_by=user, status=TicketStatus.OPEN)
        TicketFactory(created_by=user, status=TicketStatus.PROCESSING)
        TicketFactory(created_by=user, status=TicketStatus.PROCESSING)
        TicketFactory(created_by=user, status=TicketStatus.RESOLVED)
        TicketFactory(created_by=user, status=TicketStatus.CANCELLED)

        open_tickets = get_tickets(params=f"status={TicketStatus.OPEN}")
        assert len(open_tickets.json()["results"]) == 1

        processing_tickets = get_tickets(params=f"status={TicketStatus.PROCESSING}")
        assert len(processing_tickets.json()["results"]) == 2

        resolved_tickets = get_tickets(params=f"status={TicketStatus.RESOLVED}")
        assert len(resolved_tickets.json()["results"]) == 1

        cancelled_tickets = get_tickets(params=f"status={TicketStatus.CANCELLED}")
        assert len(cancelled_tickets.json()["results"]) == 1

        mixed_tickets = get_tickets(
            params=f"status={TicketStatus.PROCESSING},{TicketStatus.OPEN}"
        )
        assert len(mixed_tickets.json()["results"]) == 3

        all_tickets = get_tickets(
            params=f"status={TicketStatus.OPEN},{TicketStatus.PROCESSING},{TicketStatus.RESOLVED},{TicketStatus.CANCELLED}"
        )
        assert len(all_tickets.json()["results"]) == 5

    def test_filter_tickets_by_priority(self, authenticate, get_tickets):
        user = authenticate()
        TicketFactory(created_by=user, priority=TicketPriority.MEDIUM)
        TicketFactory(created_by=user, priority=TicketPriority.MEDIUM)
        TicketFactory(created_by=user, priority=TicketPriority.HIGH)
        TicketFactory(created_by=user, priority=TicketPriority.NORMAL)

        normal_tickets = get_tickets(params=f"priority={TicketPriority.NORMAL}")
        assert len(normal_tickets.json()["results"]) == 1

        medium_tickets = get_tickets(params=f"priority={TicketPriority.MEDIUM}")
        assert len(medium_tickets.json()["results"]) == 2

        high_tickets = get_tickets(params=f"priority={TicketPriority.HIGH}")
        assert len(high_tickets.json()["results"]) == 1

        mixed_tickets = get_tickets(
            params=f"priority={TicketPriority.MEDIUM},{TicketPriority.HIGH}"
        )
        assert len(mixed_tickets.json()["results"]) == 3

        all_tickets = get_tickets(
            params=f"priority={TicketPriority.NORMAL},{TicketPriority.MEDIUM},{TicketPriority.HIGH}"
        )
        assert len(all_tickets.json()) == 4

    def test_filter_tickets_by_page_and_page_size(self, authenticate, get_tickets):
        user = authenticate()
        TicketFactory(created_by=user)
        TicketFactory(created_by=user)
        TicketFactory(created_by=user)
        TicketFactory(created_by=user)

        first_page_tickets = get_tickets(params="page=1&page_size=2")
        assert len(first_page_tickets.json()["results"]) == 2

        second_page_tickets = get_tickets(params="page=2&page_size=2")
        assert len(second_page_tickets.json()["results"]) == 2

    def test_filter_tickets_by_project(self, authenticate, get_tickets):
        user = authenticate()
        project1 = ProjectFactory()
        project2 = ProjectFactory()
        project3 = ProjectFactory()
        project4 = ProjectFactory()
        TicketFactory(created_by=user, project=project1)
        TicketFactory(created_by=user, project=project2)
        TicketFactory(created_by=user, project=project3)
        TicketFactory(created_by=user, project=project4)

        results = get_tickets(params=f"project={project1.id},{project2.id}")
        assert len(results.json()["results"]) == 2

        results = get_tickets(params=f"project={project1.id}")
        assert len(results.json()["results"]) == 1

        results = get_tickets(
            params=f"project={project1.id},{project2.id},{project3.id},{project4.id}"
        )
        assert len(results.json()["results"]) == 4


@pytest.mark.django_db
class TestSearchTicket:
    def test_search_ticket(self, authenticate, get_tickets):
        user = authenticate()
        TicketFactory(
            created_by=user, title="First ticket", description="first description"
        )
        TicketFactory(
            created_by=user, title="Second ticket", description="second description"
        )
        TicketFactory(
            created_by=user, title="Third ticket", description="third description"
        )

        search_results_1 = get_tickets(params="search=ticket")
        assert len(search_results_1.json()["results"]) == 3

        search_results_2 = get_tickets(params="search=second")
        assert len(search_results_2.json()["results"]) == 1

        search_results_3 = get_tickets(params="search=nothing")
        assert len(search_results_3.json()["results"]) == 0
