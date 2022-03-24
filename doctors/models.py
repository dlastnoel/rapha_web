import uuid
import datetime
from django.db import models
from django.contrib.auth.models import User
from patients.models import Patient


class Specialization(models.Model):
    field = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.field


class Doctor(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)
    user = models.OneToOneField(
        User, on_delete=models.CASCADE)
    specialization = models.ForeignKey(
        Specialization, on_delete=models.SET_NULL, null=True)
    profile_image = models.ImageField(
        null=True, blank=True, upload_to='doctors/', default='doctors/doctor-default.png')
    username = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100)
    address = models.CharField(max_length=255, null=True, blank=True)
    contact = models.CharField(max_length=11, null=True, blank=True)
    email = models.EmailField(max_length=100, null=True, blank=True)
    short_bio = models.TextField(null=True, blank=True)
    is_activated = models.BooleanField(default=False, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.username


class Schedule(models.Model):
    weekday_choices = (
        ('Monday', "Monday"),
        ('Tuesday', "Tuesday"),
        ('Wednesday', "Wednesday"),
        ('Thursday', "Thursday"),
        ('Friday', "Friday"),
        ('Saturday', "Saturday"),
        ('Sunday', "Sunday"),
    )

    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    weekday = models.CharField(
        max_length=100,  choices=weekday_choices)
    start = models.TimeField(null=True, blank=True)
    end = models.TimeField(null=True, blank=True)

    def __str__(self):
        return self.doctor.first_name


class Slot(models.Model):
    limit = models.DateField(null=True, blank=True)
