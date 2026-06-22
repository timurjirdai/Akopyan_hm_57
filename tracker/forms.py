from django import forms
from .models import Issue, Status, Type, Project

class IssueForm(forms.ModelForm):
    status = forms.ModelChoiceField(
        queryset=Status.objects.all()
    )

    types = forms.ModelMultipleChoiceField(
        queryset=Type.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Issue
        exclude = ['project', 'is_deleted']


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = '__all__'