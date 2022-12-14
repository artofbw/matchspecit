class TestUserModel:
    def test_user_str_returns_name(self, create_user):
        user = create_user(username="test_name")

        assert user.__str__() == "test_name"

    def test_user_delete_set_active_and_matchable_to_false(self, create_user):
        user = create_user()

        assert user.is_active
        assert user.is_matchable

        user.delete()

        assert not user.is_active
        assert not user.is_matchable
