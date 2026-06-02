"""Project DRF serializer."""

from rest_framework import serializers

from projects.models import Project


class ProjectSerializer(serializers.ModelSerializer):
    """Serializer for the Project model."""

    class Meta:
        model = Project
        fields = ("id", "author", "title", "description", "status", "pub_date", "participants")
        read_only_fields = ("author", "pub_date")
