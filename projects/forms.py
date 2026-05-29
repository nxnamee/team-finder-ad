from django import forms
from .models import Project


class ListingForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ('title', 'description', 'status', 'skills')
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
        }

    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)
        for f in self.fields.values():
            f.widget.attrs.update({'class': 'pf-input'})
