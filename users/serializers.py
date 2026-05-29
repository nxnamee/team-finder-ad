from rest_framework import serializers
from .models import CustomUser


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'bio', 'avatar', 'github', 'linkedin', 'website', 'skills', 'role')
        read_only_fields = ('id',)
