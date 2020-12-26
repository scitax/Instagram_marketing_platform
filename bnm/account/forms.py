from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from django import forms
from django.views.generic.edit import ModelFormMixin
from .models import User, Add_posting


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['email', 'usertype', 'password1', 'password1']

class Add_posting_form(ModelForm):
    class Meta:
        model = Add_posting
        fields = ['title', 'description', 'platforms']
