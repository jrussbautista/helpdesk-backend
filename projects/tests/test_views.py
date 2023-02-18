from rest_framework import status
import pytest
from projects.factories import ProjectFactory


@pytest.fixture
def get_projects(api_client):
    def do_get_projects():
        return api_client.get("/projects/")

    return do_get_projects


@pytest.fixture
def get_project(api_client):
    def do_get_project(id):
        return api_client.get(f"/projects/{id}/")

    return do_get_project


@pytest.fixture
def create_project(api_client):
    def do_create_project(id):
        return api_client.post(
            "/projects/",
            id,
        )

    return do_create_project


@pytest.fixture
def update_project(api_client):
    def do_update_project(id, payload):
        return api_client.put(
            f"/projects/{id}/",
            payload,
        )

    return do_update_project


@pytest.fixture
def delete_project(api_client):
    def do_delete_project(id):
        return api_client.delete(f"/projects/{id}/")

    return do_delete_project


@pytest.fixture
def user_project(authenticate):
    user = authenticate()
    project = ProjectFactory(owner=user)
    return project


@pytest.mark.django_db
class TestViewProjects:
    def test_logged_in_user_can_view_owned_projects(self, authenticate, get_projects):
        user = authenticate()
        project1 = ProjectFactory(owner=user)
        ProjectFactory(owner=user)
        response = get_projects()
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2
        assert response.data[0]["name"] == project1.name
        assert response.data[0]["description"] == project1.description

    def test_logged_in_user_can_view_owned_individual_project(
        self, user_project, get_project
    ):
        response = get_project(user_project.id)
        assert response.data["name"] == user_project.name
        assert response.data["description"] == user_project.description
        assert response.status_code == status.HTTP_200_OK

    def test_cannot_view_someones_projects(self, authenticate, get_projects):
        authenticate()
        ProjectFactory()
        response = get_projects()
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 0

    def test_cannot_view_someones_individual_project(self, authenticate, get_project):
        project = ProjectFactory()
        authenticate()
        response = get_project(project.id)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_anonymous_user_cannot_view_projects(self, get_projects):
        response = get_projects()
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_anonymous_user_cannot_view_individual_project(self, get_project):
        project = ProjectFactory()
        response = get_project(project.id)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestCreateProject:
    def test_logged_in_user_can_create_project(self, authenticate, create_project):
        authenticate()
        payload = {"name": "Test Project", "description": "test project description"}
        response = create_project(payload)
        assert response.status_code == status.HTTP_201_CREATED

    def test_cannot_create_project_if_data_is_invalid(
        self, authenticate, create_project
    ):
        authenticate()
        payload = {"name": "", "description": ""}
        response = create_project(payload)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_anonymous_user_cannot_create_project(self, create_project):
        payload = {"name": "Test Project", "description": "test project description"}
        response = create_project(payload)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestUpdateProject:
    def test_logged_in_user_can_update_project(self, user_project, update_project):
        payload = {"name": "Update title", "description": "updated description"}
        response = update_project(user_project.id, payload)
        assert response.status_code == status.HTTP_200_OK

    def test_cannot_update_project_if_data_is_invalid(
        self, user_project, update_project
    ):
        payload = {"name": "", "description": ""}
        response = update_project(user_project.id, payload)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_should_not_be_able_to_delete_someones_project(
        self, authenticate, update_project
    ):
        project_by_someone = ProjectFactory()
        authenticate()
        payload = {"name": "Update title", "description": "updated description"}
        response = update_project(project_by_someone.id, payload)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_anonymous_user_cannot_update_project(self, update_project):
        project = ProjectFactory()
        payload = {"name": "Test Project", "description": "test project description"}
        response = update_project(project.id, payload)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestDeleteProject:
    def test_logged_in_user_can_delete_project(self, user_project, delete_project):
        response = delete_project(user_project.id)
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_should_not_be_able_to_delete_someones_project(
        self, authenticate, delete_project
    ):
        authenticate()
        project_by_someone = ProjectFactory()
        response = delete_project(project_by_someone.id)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_anonymous_user_cannot_delete_project(self, delete_project):
        project = ProjectFactory()
        response = delete_project(project.id)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
