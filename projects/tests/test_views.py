from authentication.models import User
from rest_framework.status import HTTP_401_UNAUTHORIZED, HTTP_201_CREATED
from rest_framework.test import APIClient
import pytest


@pytest.mark.django_db
class TestCreateProject:
    def test_anonymous_user_cannot_create_project(self):
        client = APIClient()
        response = client.post(
            "/projects/",
            {"name": "Test Project", "description": "test project description"},
        )
        assert response.status_code == HTTP_401_UNAUTHORIZED

    def test_logged_in_user_can_create_project(self, django_user_model):
        client = APIClient()
        user = django_user_model.objects.create(
            username="test_username", password="test_password"
        )
        client.force_authenticate(user=user)
        response = client.post(
            "/projects/",
            {"name": "Test Project", "description": "test project description"},
        )
        assert response.status_code == HTTP_201_CREATED
