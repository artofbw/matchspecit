from rest_framework import permissions


class OwnProfilePermission(permissions.BasePermission):
    """
    Object-level permission to only allow access user own profile
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # obj here is an own user instance
        return obj.user == request.user


class IsActive(permissions.BasePermission):
    """
    Allows access only to the active users.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_active)
