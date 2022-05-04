import pytest

from matchspecit.user.serializers import UserSerializer


@pytest.mark.django_db
class TestUserSerializer:
    serializer = UserSerializer

    def test_serializer_returns_validation_error(self, create_user):
        user = create_user()
        serializer = self.serializer(instance=user, data={})

        assert not serializer.is_valid()
        assert set(serializer.errors.keys()) == {"is_matchable", "technologies"}

    def test_serializer_returns_updated_fields(self, create_user, create_technologies):
        technologies = create_technologies()
        user = create_user()

        selected_technologies = [technologies.values("id", "name")[0]]
        data = {"technologies": selected_technologies, "is_matchable": True}

        serializer = self.serializer(instance=user, data=data)
        serializer.is_valid()

        updated_user = serializer.update(user, serializer.validated_data)

        assert updated_user.technologies.all()[0].id == technologies[0].id
        assert updated_user.is_matchable
