from django import forms
from django.contrib.auth.models import User

from .models import Presentation, Slide

class PresentationForm(forms.ModelForm):

    class Meta:
        model = Presentation
        fields = ['title', 'description', 'pdf_file']


class SlideForm(forms.ModelForm):

    class Meta:
        model = Slide
        fields = ['image_file', 'order']


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
