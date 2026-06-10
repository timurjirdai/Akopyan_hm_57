from django import forms
from .models import Issue, Status, Type


class IssueForm(forms.ModelForm):
    status = forms.ModelChoiceField(
        queryset=Status.objects.all()
    )

    type = forms.ModelChoiceField(
        queryset=Type.objects.all()
    )

    class Meta:
        model = Issue
        fields = '__all__'