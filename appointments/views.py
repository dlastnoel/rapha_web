from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from . forms import AppointmentForm

from patients.models import AdultIllness, Breast, Cardiovascular, ChiefComplaint, ChildhoodIllness, Endocrine, FamilyHistory, FunctionalHistory, Gastrointestinal, GeneralSystem, Genitourinary, Heent, HistoryOfImmunization, Musculoskeletal, Neurologic, PresentIllness, PresentIllnessImage, Pulmonary, SkinProblem
from . models import *
from appointments.models import Appoinment
from datetime import date, datetime


# Create your views here.
@login_required(login_url='login')
def appointments(request):
    title = 'Appointments'
    is_admin = request.user.is_superuser
    today = date.today()
    patients_today = Appoinment.objects.filter(
        doctor=request.user.doctor).filter(checkup_date=today)
    ages_today = []
    i = 0

    print(patients_today.count())

    while(i < patients_today.count()):
        ages_today.append(today.year - patients_today[i].patient.date_of_birth.year -
                          ((today.month, today.day) < (
                              patients_today[i].patient.date_of_birth.month, patients_today[i].patient.date_of_birth.day)))
        i = i+1

    doctor = request.user.doctor
    nav_active = 'nav-active'
    context = {
        'title': title,
        'doctor': doctor,
        'is_admin': is_admin,
        'nav_active': nav_active,
        'patients_today': patients_today,
        'appointments_today': zip(patients_today, ages_today)
    }
    return render(request, 'appointments/index.html', context)


@login_required(login_url='login')
def appointment(request, pk):
    title = 'Appointments'
    is_admin = request.user.is_superuser
    patient = Appoinment.objects.get(id=pk)
    doctor = request.user.doctor
    nav_active = 'nav-active'
    chief_complaint = ChiefComplaint.objects.get(unicode=patient.unicode)
    present_illness_image = PresentIllnessImage.objects.get(
        unicode=patient.unicode)
    present_illness = PresentIllness.objects.get(unicode=patient.unicode)
    childhood_illness = ChildhoodIllness.objects.get(unicode=patient.unicode)
    adult_illness = AdultIllness.objects.get(unicode=patient.unicode)
    history_of_immunization = HistoryOfImmunization.objects.get(
        unicode=patient.unicode)
    family_history = FamilyHistory.objects.get(unicode=patient.unicode)
    personal_and_social_history = ChiefComplaint.objects.get(
        unicode=patient.unicode)
    functional_history = FunctionalHistory.objects.get(unicode=patient.unicode)
    generay_system = GeneralSystem.objects.get(unicode=patient.unicode)
    skin_problem = SkinProblem.objects.get(unicode=patient.unicode)
    heent = Heent.objects.get(unicode=patient.unicode)
    breast = Breast.objects.get(unicode=patient.unicode)
    pulmonary = Pulmonary.objects.get(unicode=patient.unicode)
    cardiovascular = Cardiovascular.objects.get(unicode=patient.unicode)
    gastrointestinal = Gastrointestinal.objects.get(unicode=patient.unicode)
    genitourinary = Genitourinary.objects.get(unicode=patient.unicode)
    endocrine = Endocrine.objects.get(unicode=patient.unicode)
    musculoskeletal = Musculoskeletal.objects.get(unicode=patient.unicode)
    neurologic = Neurologic.objects.get(unicode=patient.unicode)

    admit = AppointmentForm(instance=patient)

    context = {
        'title': title,
        'doctor': doctor,
        'is_admin': is_admin,
        'nav_active': nav_active,
        'patient': patient,
        'chief_complaint': chief_complaint,
        'present_illness_image': present_illness_image,
        'present_illness': present_illness,
        'childhood_illness': childhood_illness,
        'adult_illness': adult_illness,
        'history_of_immunization': history_of_immunization,
        'family_history': family_history,
        'personal_and_social_history': personal_and_social_history,
        'functional_history': functional_history,
        'generay_system': generay_system,
        'skin_problem': skin_problem,
        'heent': heent,
        'breast': breast,
        'pulmonary': pulmonary,
        'cardiovascular': cardiovascular,
        'gastronintestinal': gastrointestinal,
        'genitourinary': genitourinary,
        'endocrine': endocrine,
        'musculoskeletal': musculoskeletal,
        'neurologic': neurologic,
        'admit': admit
    }
    return render(request, 'appointments/appointment.html', context)


@login_required(login_url='login')
def admitPatient(request, pk):
    patient = Appoinment.objects.get(id=pk)
    if request.method == 'POST':
        admit = AppointmentForm(
            request.POST, instance=patient)
        if admit.is_valid():
            patient.status = 'done'
            patient.save()
            admit.save()
            return redirect('appointments')
