"""Custom DRF permission."""

from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    """Allow write access only to the project author."""

    def has_object_permission(self, request, view, obj):
        """Read for everyone, write for author only."""
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user
