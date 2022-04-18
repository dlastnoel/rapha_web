from random import choices
from django.forms import ModelForm, fields
from . models import Appoinment
from doctors.models import Doctor
from django import forms


class AppointmentForm(ModelForm):
    class Meta:
        model = Appoinment
        fields = ['statement']

    def __init__(self, *args, **kwargs):
        super(AppointmentForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})


class CancelAppointmentForm(forms.Form):
    doctor = forms.ChoiceField(label='Doctor')
    message = forms.CharField(widget=forms.Textarea)

    def __init__(self, doctor_choices, *args, **kwargs):
        choices = doctor_choices
        super(CancelAppointmentForm, self).__init__(*args, **kwargs)
        self.fields['doctor'].choices = choices

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
