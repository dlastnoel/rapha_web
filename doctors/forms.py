from django.forms import ModelForm, fields
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm
from django.contrib.auth.models import User
from . models import *
from django import forms


class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email',
                  'username', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})


class UserPasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super(UserPasswordResetForm, self).__init__(*args, **kwargs)

    email = forms.EmailField(label='Email address', widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'example@email.com',
        'type': 'email',
        'name': 'email'
    }))


class DoctorForm(ModelForm):
    class Meta:
        model = Doctor
        fields = ['specialization', 'middle_name',
                  'address', 'contact', 'schedule', 'short_bio']

    def __init__(self, *args, **kwargs):
        super(DoctorForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})


class NewDoctorForm(ModelForm):
    class Meta:
        model = Doctor
        fields = ['specialization', 'profile_image', 'middle_name',
                  'address', 'contact', 'schedule', 'short_bio']

    def __init__(self, *args, **kwargs):
        super(NewDoctorForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})


class SpecilizationForm(ModelForm):
    class Meta:
        model = Specialization
        fields = ['field']

    def __init__(self, *args, **kwargs):
        super(SpecilizationForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
