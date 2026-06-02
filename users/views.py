"""DRF views for the users API."""

from django.contrib.auth import get_user_model
from rest_framework import permissions, viewsets

from team_finder.constants import (
    FILTER_FAV_AUTHORS,
    FILTER_LIKERS_OF_MY_PROJECTS,
    FILTER_MY_PARTICIPATION,
    FILTER_PARTICIPANTS_OF_MY_PROJECTS,
)
from users.serializers import UserSerializer

User = get_user_model()


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """Read-only user list/detail with query-param filtering."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        """Apply optional filter based on query parameter."""
        qs = super().get_queryset()
        fltr = self.request.query_params.get("filter")
        if not fltr or not self.request.user.is_authenticated:
            return qs

        usr = self.request.user
        if fltr == FILTER_FAV_AUTHORS:
            return qs.filter(projects__favorited_by=usr).distinct()
        if fltr == FILTER_MY_PARTICIPATION:
            return qs.filter(projects__participants=usr).distinct()
        if fltr == FILTER_LIKERS_OF_MY_PROJECTS:
            return qs.filter(favorite_projects__author=usr).distinct()
        if fltr == FILTER_PARTICIPANTS_OF_MY_PROJECTS:
            return qs.filter(joined_projects__author=usr).distinct()

        return qs
