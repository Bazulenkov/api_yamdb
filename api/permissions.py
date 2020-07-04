from rest_framework.permissions import BasePermission, SAFE_METHODS, IsAuthenticatedOrReadOnly


class IsAdminRole(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user.is_superuser
            or request.auth and request.user.role == "admin"
        )


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS
            or request.user.is_superuser
            or request.auth and request.user.role == "admin"
        )


class IsStaffOrOwnerOrReadOnly(IsAuthenticatedOrReadOnly):
    def has_object_permission(self, request, view, obj):
        return bool(
            obj.author == request.user
            or request.method in SAFE_METHODS
            or request.auth and request.user.role == "admin"
            or request.auth and request.user.role == "moderator"
        )
