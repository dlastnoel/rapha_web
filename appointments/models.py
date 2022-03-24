import uuid
from django.db import models
from doctors.models import Doctor
from patients.models import Patient
# Create your models here.


class Appoinment(models.Model):
    status_choices = (
        ('none', "None"),
        ('cancelled', "Cancelled"),
        ('done', "Done")
    )

    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(
        Doctor, on_delete=models.CASCADE, null=True, blank=True)
    unicode = models.CharField(max_length=300, null=True)
    checkup_date = models.DateField(null=True, blank=True)
    checkup_time = models.TimeField(null=True, blank=True)
    status = models.CharField(
        max_length=100,  choices=status_choices, default='none')
    statement = models.TextField(null=True, blank=True)
