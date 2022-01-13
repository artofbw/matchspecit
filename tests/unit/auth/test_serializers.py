import pytest
from django.contrib.auth import get_user_model

from matchspecit.auth.serializers import (
    MyTokenObtainPairSerializer,
    RegisterSerializer
)


class TestMyTokenObtainPairSerializer:
    serializer = MyTokenObtainPairSerializer

    def test_serializer_assign_username_to_token(self, create_user):
        user = create_user()
        token = self.serializer.get_token(user)

        assert token["username"] == user.username


@pytest.mark.django_db
class TestRegisterSerializer:
    serializer = RegisterSerializer

    def test_serializer_returns_validation_error_for_different_passwords(self):
        data = {
            "username": "test_username",
            "password": "5tr0ngPassword123!!",
            "password2": "DummyIncorrectPassword",
            "email": "test@fake.com",
            "first_name": "Test",
            "last_name": "Fake",
        }
        serializer = self.serializer(data=data)

        assert not serializer.is_valid()
        assert set(serializer.errors.keys()) == {"password"}

    def test_serializer_returns_user(self):
        expected_result = {
            "username": "test_username",
            "email": "test@fake.com",
            "first_name": "Test",
            "last_name": "Fake",
        }
        data = {
            "username": "test_username",
            "password": "5tr0ngPassword123!!",
            "password2": "5tr0ngPassword123!!",
            "email": "test@fake.com",
            "first_name": "Test",
            "last_name": "Fake",
        }
        serializer = self.serializer(data=data)

        serializer.is_valid()

        assert serializer.data == expected_result

    def test_serializer_create_returns_user_instance(self):
        data = {
            "username": "test_username",
            "password": "5tr0ngPassword123!!",
            "password2": "5tr0ngPassword123!!",
            "email": "test@fake.com",
            "first_name": "Test",
            "last_name": "Fake",
        }
        serializer = self.serializer(data=data)
        serializer.is_valid()
        user = serializer.create(serializer.validated_data)

        assert isinstance(user, get_user_model())
