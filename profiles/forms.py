# forms.py
from django import forms
from django.contrib.auth.models import User
from .models import Profile

class UserForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'w-full p-2 border rounded',
    }))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'w-full p-2 border rounded',
    }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'w-full p-2 border rounded',
    }))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

class ProfileForm(forms.ModelForm):
    bio = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'w-full p-2 border rounded',
        'rows': 4,
    }))
    location = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'w-full p-2 border rounded',
    }))
    birth_date = forms.DateField(widget=forms.DateInput(attrs={
        'class': 'w-full p-2 border rounded',
        'type': 'date',
    }))

    class Meta:
        model = Profile
        fields = ('bio', 'location', 'birth_date', 'avatar')