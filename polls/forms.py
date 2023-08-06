from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db import models


class SignUpForm(UserCreationForm):
    age = forms.IntegerField()
    
    class Meta:
        model = User
        fields = ("username", "password1", "password2", "age")

    def save(self, commit=True):
        user = super().save(commit=commit)
        return user
