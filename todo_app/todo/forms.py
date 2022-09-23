from django import forms

from django.forms import ModelForm
from django.contrib.auth.models import User


class UserUpdateForm(ModelForm):
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name']
