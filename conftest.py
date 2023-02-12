from rest_framework.test import APIClient
import pytest


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def authenticate(api_client, django_user_model):
    def do_authenticate():
        user = django_user_model.objects.create(
            username="test_username", password="test_password"
        )
        return api_client.force_authenticate(user=user)

    return do_authenticate
