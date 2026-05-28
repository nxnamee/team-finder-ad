from http import HTTPStatus

from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

from projects.models import Project
from projects.permissions import IsAuthorOrReadOnly
from projects.serializers import ProjectSerializer


class ProjectViewSet(viewsets.ModelViewSet):

    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsAuthorOrReadOnly]
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['post', 'delete'],
            permission_classes=[permissions.IsAuthenticated])
    def favorite(self, request, pk=None):
        project = self.get_object()
        if request.method == 'POST':
            project.favorited_by.add(request.user)
            return Response({'status': 'added to favorites'},
                            status=HTTPStatus.CREATED)
        elif request.method == 'DELETE':
            project.favorited_by.remove(request.user)
            return Response({'status': 'removed from favorites'},
                            status=HTTPStatus.NO_CONTENT)
        return Response(status=HTTPStatus.METHOD_NOT_ALLOWED)
