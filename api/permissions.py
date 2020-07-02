from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):  # has_permission(self, request, view):
        return request.user.role == "admin"

    def has_permission(self, request, view):
        # if view.action == 'list':# or view.action == 'create':
        return request.user.role == "admin"
        # return True


class IsModerator(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.role == "moderator"
