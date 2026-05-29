from rest_framework import viewsets, permissions
from .models import CustomUser
from .serializers import MemberSerializer


class MemberViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = MemberSerializer
    permission_classes = [permissions.AllowAny]
