import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken


@pytest.mark.django_db
class TestLogin:
    url = reverse('token_obtain_pair')

    def test_login_success_returns_access_and_refresh_token(
        self, api_client, create_user, test_password
    ):
        user = create_user()
        response = api_client.post(
            self.url,
            data={"username": user.username, "password": test_password}
        )

        assert response.status_code == status.HTTP_200_OK
        assert "refresh" in response.json()
        assert "access" in response.json()

    def test_login_incorrect_credentials_returns_unauthorized(self, api_client):
        response = api_client.post(
            self.url,
            data={"username": "incorrect_username", "password": "fake_pass"}
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.json()["detail"] == "No active account found with the given credentials"


class TestLoginRefresh:
    url = reverse("token_refresh")

    def test_login_refresh_returns_new_tokens(self, api_client, create_user):
        user = create_user()
        token = RefreshToken.for_user(user)
        response = api_client.post(self.url, data={"refresh": str(token)})

        assert response.status_code == status.HTTP_200_OK
        assert "access" in response.json()

    def test_login_refresh_return_unauthorized_for_invalid_token(self, api_client):
        response = api_client.post(self.url, data={"refresh": "123"})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.json()["detail"] == "Token is invalid or expired"
        assert response.json()["code"] == "token_not_valid"


@pytest.mark.django_db
class TestRegister:
    url = reverse("auth_register")

    def test_register_returns_user_data(self, api_client):
        expected_result = {'username': 'test_user', 'email': 'test@fake.com', 'first_name': 'Test', 'last_name': 'Fake'}

        response = api_client.post(
            self.url,
            data={
                "username": "test_user",
                "password": "5tr0ngPass1!",
                "password2": "5tr0ngPass1!",
                "email": "test@fake.com",
                "first_name": "Test",
                "last_name": "Fake"
            }
        )

        assert response.status_code == status.HTTP_201_CREATED
        assert response.json() == expected_result

    def test_register_invalid_data_returns_bad_request(self, api_client):
        expected_result = {
            'username': ['This field may not be blank.'],
            'password': ['This field may not be blank.'],
            'password2': ['This field may not be blank.'],
            'email': ['This field may not be blank.'],
        }

        response = api_client.post(
            self.url,
            data={
                "username": "",
                "password": "",
                "password2": "",
                "email": "",
                "first_name": "",
                "last_name": ""
            }
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == expected_result

    def test_register_returns_validation_message_for_different_password(self, api_client):
        expected_result = {'password': ['Hasła nie są takie same.']}

        response = api_client.post(
            self.url,
            data={
                "username": "test_user",
                "password": "5tr0ngPass1!",
                "password2": "IncorrectPassword",
                "email": "test@fake.com",
                "first_name": "Test",
                "last_name": "Fake"
            }
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == expected_result
