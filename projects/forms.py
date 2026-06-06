"""Project creation and editing form."""

from django import forms

from projects.models import Project


def _validate_github_url(value):
    """Ensure the URL points to github.com."""
    if value and "github.com" not in value.lower():
        raise forms.ValidationError("Ссылка должна вести на github.com")


class ProjectForm(forms.ModelForm):
    """Form for creating and editing projects."""

    github = forms.URLField(
        label="GitHub",
        required=False,
        validators=[_validate_github_url],
    )

    class Meta:
        model = Project
        fields = ("title", "description", "github", "status")
