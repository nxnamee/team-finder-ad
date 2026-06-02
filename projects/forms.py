"""Project creation and editing form."""

from django import forms

from projects.models import Project


class ProjectForm(forms.ModelForm):
    """Form for creating and editing projects."""

    class Meta:
        model = Project
        fields = ("title", "description", "github", "status")
