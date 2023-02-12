from rest_framework.test import APIClient
import pytest
from authentication.factories import UserFactory


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def authenticate(api_client):
    def do_authenticate():
        user = UserFactory()
        return api_client.force_authenticate(user=user)

    return do_authenticate
