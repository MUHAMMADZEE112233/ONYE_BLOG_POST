from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import *


class UserAdminCreationForm(UserCreationForm):
    """
    A Custom form for creating new users.
    """

    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name',  'date_of_birth', 'password1', 'password2']


class CustomUserChangeForm(UserChangeForm):
    password = None # This is to remove the password field from the form

    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'date_of_birth']


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'category']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'email', 'body']
