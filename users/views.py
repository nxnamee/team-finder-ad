from django.contrib.auth import get_user_model
from rest_framework import permissions, viewsets

from users.serializers import UserSerializer

User = get_user_model()


class UserViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        base_queryset = super().get_queryset()
        filter_param = self.request.query_params.get('filter')
        if not filter_param or not self.request.user.is_authenticated:
            return base_queryset

        current_user = self.request.user
        if filter_param == 'fav_authors':
            return base_queryset.filter(projects__favorited_by=current_user).distinct()
        if filter_param == 'my_participation':
            return base_queryset.filter(projects__participants=current_user).distinct()
        if filter_param == 'likers_of_my_projects':
            return base_queryset.filter(favorite_projects__author=current_user).distinct()
        if filter_param == 'participants_of_my_projects':
            return base_queryset.filter(joined_projects__author=current_user).distinct()

        return base_queryset
