import pytest
from django.forms import model_to_dict
from django.urls import reverse
from rest_framework import status


def project_to_dict(project):
    return model_to_dict(project, exclude=["_state", "id"])


@pytest.mark.django_db
class TestProjectView:
    url = reverse("project_view")

    def test_project_post_return_project(self, api_client, create_user, test_password):
        expected_result = {'serializer.data': 200, 'status': 201}
        user = create_user()
        api_client.force_authenticate(user=user)

        response = api_client.post(self.url, data={"name": "test project"})

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == expected_result

    def test_project_get_return_list_of_projects(self, api_client, create_user, test_password, create_project):
        project = create_project()
        user = create_user()
        api_client.force_authenticate(user=user)

        response = api_client.get(self.url, data={"name": "test project"})

        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.json(), list)
        assert len(response.json()) == 1
        assert response.json()[0] == project_to_dict(project)


@pytest.mark.django_db
class TestProjectDetail:
    url_namespace = "project_detail"

    def test_project_detail_get_by_id_return_project(self, api_client, create_user, test_password, create_project):
        project = create_project()
        url = reverse(self.url_namespace, args=[project.id])
        user = create_user()
        api_client.force_authenticate(user=user)

        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == project_to_dict(project)

    def test_project_detail_get_by_incorrect_id_return_not_found(self, api_client, create_user, test_password):
        url = reverse(self.url_namespace, args=[9999])
        user = create_user()
        api_client.force_authenticate(user=user)

        response = api_client.get(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json() == {'detail': 'Not found.'}

    def test_project_detail_put_by_id_update_project(self, api_client, create_user, test_password, create_project):
        project = create_project()
        url = reverse(self.url_namespace, args=[project.id])
        user = create_user()
        api_client.force_authenticate(user=user)

        response = api_client.put(url, data={"name": "test updated name"})
        project.refresh_from_db()

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == project_to_dict(project)

    def test_project_detail_put_by_incorrect_id_return_not_found(self, api_client, create_user, test_password):
        url = reverse(self.url_namespace, args=[9999])
        user = create_user()
        api_client.force_authenticate(user=user)

        response = api_client.put(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json() == {'detail': 'Not found.'}

    def test_project_detail_delete_by_id_removes_project(self, api_client, create_user, test_password, create_project):
        project = create_project()
        url = reverse(self.url_namespace, args=[project.id])
        user = create_user()
        api_client.force_authenticate(user=user)

        response = api_client.delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_project_detail_delete_by_incorrect_id_return_not_found(self, api_client, create_user, test_password):
        url = reverse(self.url_namespace, args=[9999])
        user = create_user()
        api_client.force_authenticate(user=user)

        response = api_client.put(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json() == {'detail': 'Not found.'}
