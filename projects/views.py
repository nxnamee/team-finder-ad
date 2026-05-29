from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Project, Membership, Favorite
from .serializers import ListingSerializer, MembershipSerializer, FavoriteSerializer


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, r, v, obj):
        if r.method in permissions.SAFE_METHODS:
            return True
        return obj.author == r.user


class ListingViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ListingSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, s):
        s.save(author=self.request.user)

    @action(detail=True, methods=['post'])
    def join(self, r, pk=None):
        p = self.get_object()
        if p.status != 'active':
            return Response({'error': 'closed'}, status=status.HTTP_400_BAD_REQUEST)
        m, created = Membership.objects.get_or_create(project=p, user=r.user)
        if not created:
            return Response({'error': 'already joined'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(MembershipSerializer(m).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def leave(self, r, pk=None):
        p = self.get_object()
        cnt, _ = Membership.objects.filter(project=p, user=r.user).delete()
        if not cnt:
            return Response({'error': 'not a member'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['post'])
    def bookmark(self, r, pk=None):
        p = self.get_object()
        f, created = Favorite.objects.get_or_create(user=r.user, project=p)
        if not created:
            f.delete()
            return Response({'liked': False})
        return Response({'liked': True})

    @action(detail=True, methods=['post'])
    def close(self, r, pk=None):
        p = self.get_object()
        if p.author != r.user:
            return Response({'error': 'not owner'}, status=status.HTTP_403_FORBIDDEN)
        p.status = 'closed'
        p.save()
        return Response({'status': 'closed'})
