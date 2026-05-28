from django import forms

from projects.models import Project
from team_finder.constants import TITLE_MAX_LENGTH


class ProjectForm(forms.ModelForm):

    name = forms.CharField(label='Название', max_length=TITLE_MAX_LENGTH)

    class Meta:
        model = Project
        fields = ('description', 'status')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk and not self.is_bound:
            self.initial['name'] = self.instance.title

    def save(self, commit=True):
        project = super().save(commit=False)
        project.title = self.cleaned_data['name']
        if commit:
            project.save()
            self.save_m2m()
        return project
