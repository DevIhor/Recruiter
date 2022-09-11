from rest_framework import permissions


class IsUserAccount(permissions.BasePermission):
    """Object-level permission to only allow users to edit their own accounts."""

    def has_object_permission(self, request, view, obj):
        return request.user == obj
