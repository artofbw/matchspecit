import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
class TestProjectDetail:
    url_namespace = "user_technologies_view"

    def test_user_is_matchable_set_to_false(self, api_client, create_user):
        url = reverse(self.url_namespace)
        user = create_user()
        api_client.force_authenticate(user=user)

        response = api_client.patch(url, data={"is_matchable": False})

        assert response.status_code == status.HTTP_200_OK
        assert response.data == {'technologies': [], 'is_matchable': False}

    def test_user_is_matchable_set_to_true(self, api_client, create_user):
        url = reverse(self.url_namespace)
        user = create_user()
        api_client.force_authenticate(user=user)

        response = api_client.patch(url, data={"is_matchable": True})

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {'technologies': [], 'is_matchable': True}

    def test_user_technologies_update(self, api_client, create_user, create_technologies):
        expected_result = {
            'technologies': [{'id': '1', 'name': 'python'}, {'id': '2', 'name': 'java'}],
            'is_matchable': True
        }
        technologies = create_technologies()
        url = reverse(self.url_namespace)
        user = create_user()
        api_client.force_authenticate(user=user)

        response = api_client.patch(url, data={"technology_ids": [technologies[0].id, technologies[1].id]})

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == expected_result

    def test_user_get_user_data(self, create_user, api_client, create_technologies):
        expected_result = {'technologies': [{'id': '1', 'name': 'python'}], 'is_matchable': True}
        technologies = create_technologies()
        url = reverse(self.url_namespace)
        user = create_user()
        user.technologies.add(technologies[0])
        api_client.force_authenticate(user=user)

        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == expected_result

    def test_user_delete_should_set_user_inactive_and_unmatchable(self, create_user, api_client):
        url = reverse(self.url_namespace)
        user = create_user()
        api_client.force_authenticate(user=user)

        response = api_client.delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not user.is_active
        assert not user.is_matchable
