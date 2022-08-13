import pytest

from matchspecit.user.serializers import UserSerializer


@pytest.mark.django_db
class TestUserSerializer:
    serializer = UserSerializer

    def test_serializer_returns_validation_error(self, create_user):
        user = create_user()
        serializer = self.serializer(instance=user, data={})

        assert not serializer.is_valid()
        assert set(serializer.errors.keys()) == {"username", "technologies"}

    def test_serializer_returns_updated_fields(self, create_user):
        user = create_user()

        data = {"is_matchable": True}

        serializer = self.serializer(instance=user, data=data)
        serializer.is_valid()

        updated_user = serializer.update(user, serializer.validated_data)

        assert updated_user.is_matchable
