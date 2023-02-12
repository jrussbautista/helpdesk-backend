from rest_framework.status import (
    HTTP_401_UNAUTHORIZED,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
)
import pytest


@pytest.fixture
def create_project(api_client):
    def do_create_project(project):
        return api_client.post(
            "/projects/",
            project,
        )

    return do_create_project


@pytest.mark.django_db
class TestCreateProject:
    def test_logged_in_user_can_create_project(self, authenticate, create_project):
        authenticate()
        response = create_project(
            {"name": "Test Project", "description": "test description"}
        )
        assert response.status_code == HTTP_201_CREATED

    def test_cannot_create_project_if_data_is_invalid(
        self, authenticate, create_project
    ):
        authenticate()
        response = create_project({"name": "", "description": ""})
        assert response.status_code == HTTP_400_BAD_REQUEST

    def test_anonymous_user_cannot_create_project(self, create_project):
        response = create_project(
            {"name": "Test Project", "description": "test project description"},
        )
        assert response.status_code == HTTP_401_UNAUTHORIZED
