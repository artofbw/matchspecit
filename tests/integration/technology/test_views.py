import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
class TestTechnologyView:
    url = reverse("technology_view")

    def test_technology_view_get_returns_list(self, api_client, create_user, create_technology):
        [create_technology() for _ in range(3)]
        user = create_user()
        api_client.force_authenticate(user=user)

        response = api_client.get(self.url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()) == 3
