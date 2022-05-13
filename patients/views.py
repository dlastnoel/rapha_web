from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from . models import Patient
from appointments.models import Appoinment
from datetime import date, datetime
# Create your views here.


@login_required(login_url='login')
def patients(request):
    title = 'Patients'
    is_admin = request.user.is_superuser
    today = date.today()
    patients = Appoinment.objects.filter(
        doctor=request.user.doctor).filter(status='done').order_by('-created_at')
    ages = []
    i = 0

    while(i < patients.count()):
        ages.append(today.year - patients[i].patient.date_of_birth.year -
                    ((today.month, today.day) < (
                        patients[i].patient.date_of_birth.month, patients[i].patient.date_of_birth.day)))
        i = i+1

    print(ages)

    doctor = request.user.doctor
    nav_active = 'nav-active'
    context = {
        'title': title,
        'doctor': doctor,
        'is_admin': is_admin,
        'nav_active': nav_active,
        'patients': patients,
        'today': today,
        'ages': ages,
        'zipped': zip(patients, ages)
    }
    return render(request, 'patients/index.html', context)
