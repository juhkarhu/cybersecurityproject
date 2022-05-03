from django import forms
from . import models
from django.contrib.auth.forms import UserCreationForm, UserModel
from django.contrib.auth import password_validation

class AddNewPost(forms.ModelForm):
    class Meta:
        model = models.Post
        fields = ['poster', 'postTitle', 'postContent', 'date']
        exclude = ['poster', 'date']

class AddProfile(forms.ModelForm):
    class Meta:
        model = models.Profile
        fields = ['bio', 'email', 'phone', 'location', 'birth_date']
        exclude = ['user']