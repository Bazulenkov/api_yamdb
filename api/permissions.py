from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminRole(BasePermission):
    def has_permission(self, request, view):
        #     # if view.action == 'list':# or view.action == 'create':
        # return request.user.role == "admin"
        return bool(
            # request.user and
            request.user.is_superuser
            or request.user.role == "admin"
        )


class CategoryPermission(BasePermission):
    def has_permission(self, request, view):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method == "GET":
            return True
        if request.user.is_anonymous:
            return False

        # Write and delete permissions are only allowed to the role=admin or django-admin
        return bool(request.user.is_superuser or request.user.role == "admin",)


class ReviewCommentPermission(BasePermission):
    def has_permission(self, request, view):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in SAFE_METHODS:
            return True
        if request.user.is_anonymous:
            return False
        return bool(request.user.is_superuser or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the snippet.
        return bool(
            obj.author == request.user
            or request.user.role == "admin"
            or request.user.role == "moderator"
        )
