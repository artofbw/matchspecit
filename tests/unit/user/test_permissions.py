from matchspecit.user.permissions import IsActive


class TestIsActivePermission:
    def test_is_active_permission_when_user_is_active(self, create_user, api_request_factory, create_view):
        view = create_view()
        user = create_user()
        api_request_factory.user = user

        permission = IsActive()

        assert permission.has_permission(api_request_factory, view)

    def test_is_active_permission_when_user_is_not_active(self, create_user, api_request_factory, create_view):
        view = create_view()
        user = create_user()
        user.delete()
        api_request_factory.user = user

        permission = IsActive()

        assert not permission.has_permission(api_request_factory, view)
