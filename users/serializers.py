"""User DRF serializer."""

from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    """Inline all profile fields on the user."""

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "avatar",
            "description",
            "phone",
            "github",
        )
