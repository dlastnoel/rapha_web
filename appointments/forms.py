from django.forms import ModelForm, fields
from . models import Appoinment
from django import forms


class AppointmentForm(ModelForm):
    class Meta:
        model = Appoinment
        fields = ['statement']

    def __init__(self, *args, **kwargs):
        super(AppointmentForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
