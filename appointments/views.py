from site import addsitepackages
from time import strftime
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from . forms import AppointmentForm, CancelAndReferAppointmentForm, CancelAppointmentForm
import requests
from doctors.models import Doctor
import json

from patients.models import *
from . models import *
from appointments.models import Appoinment
from datetime import date, datetime, timedelta


# Create your views here.
@login_required(login_url='login')
def appointments(request):
    title = 'Appointments'
    is_admin = request.user.is_superuser
    today = date.today()
    patients_today = Appoinment.objects.filter(
        doctor=request.user.doctor).filter(checkup_date=today)
    ages_today = []
    patients_tomorrow = Appoinment.objects.filter(
        doctor=request.user.doctor).filter(checkup_date=today+timedelta(days=1))
    ages_tomorrow = []
    i = 0

    # print(patients_today.count())

    while(i < patients_today.count()):
        ages_today.append(today.year - patients_today[i].patient.date_of_birth.year -
                          ((today.month, today.day) < (
                              patients_today[i].patient.date_of_birth.month, patients_today[i].patient.date_of_birth.day)))
        i = i+1
    i = 0

    while(i < patients_tomorrow.count()):
        ages_tomorrow.append(today.year - patients_tomorrow[i].patient.date_of_birth.year -
                             ((today.month, today.day) < (
                              patients_tomorrow[i].patient.date_of_birth.month, patients_tomorrow[i].patient.date_of_birth.day)))
        i = i+1

    doctor = request.user.doctor
    nav_active = 'nav-active'
    context = {
        'title': title,
        'doctor': doctor,
        'is_admin': is_admin,
        'nav_active': nav_active,
        'patients_today': patients_today,
        'patients_tomorrow': patients_tomorrow,
        'appointments_today': zip(patients_today, ages_today),
        'appointments_tomorrow': zip(patients_tomorrow, ages_tomorrow)
    }
    return render(request, 'appointments/index.html', context)


@login_required(login_url='login')
def futureAppointments(request):
    title = 'Appointments'
    is_admin = request.user.is_superuser
    today = date.today()
    patients = Appoinment.objects.filter(
        doctor=request.user.doctor).filter(checkup_date__gte=today+timedelta(days=2), checkup_date__lte=today+timedelta(days=14))
    ages = []
    i = 0

    while(i < patients.count()):
        ages.append(today.year - patients[i].patient.date_of_birth.year -
                    ((today.month, today.day) < (
                        patients[i].patient.date_of_birth.month, patients[i].patient.date_of_birth.day)))
        i = i+1

    doctor = request.user.doctor
    nav_active = 'nav-active'
    context = {
        'title': title,
        'doctor': doctor,
        'is_admin': is_admin,
        'nav_active': nav_active,
        'patients': patients,
        'appointments': zip(patients, ages),
    }
    return render(request, 'appointments/future.html', context)


@login_required(login_url='login')
def appointment(request, pk):
    title = 'Appointments'
    is_admin = request.user.is_superuser
    patient_appointment = Appoinment.objects.get(id=pk)
    today = date.today()
    appointment_date = patient_appointment.checkup_date
    doctors = Doctor.objects.exclude(id=request.user.doctor.id)
    doctor_choices = []
    for doctor in doctors:
        temp = (str(doctor.id), doctor.first_name + ' ' +
                doctor.last_name + ' (' + doctor.specialization.field + ')')
        doctor_choices.append(temp)

    cancel_appointment_form = CancelAppointmentForm()
    cancel_and_refer_form = CancelAndReferAppointmentForm(doctor_choices)
    previous_appointments = Appoinment.objects.filter(patient=patient_appointment.patient).filter(status='done').exclude(
        unicode=patient_appointment.unicode)
    patient = patient_appointment.patient
    doctor = request.user.doctor
    nav_active = 'nav-active'
    chief_complaint = ChiefComplaint.objects.get(
        unicode=patient_appointment.unicode)
    present_illness_image = PresentIllnessImage.objects.get(
        unicode=patient_appointment.unicode)
    present_illness = PresentIllness.objects.get(
        unicode=patient_appointment.unicode)
    childhood_illness = ChildhoodIllness.objects.get(
        unicode=patient_appointment.unicode)
    adult_illness = AdultIllness.objects.get(
        unicode=patient_appointment.unicode)
    history_of_immunization = HistoryOfImmunization.objects.get(
        unicode=patient_appointment.unicode)
    family_history = FamilyHistory.objects.get(
        unicode=patient_appointment.unicode)
    personal_and_social_history = PersonalAndSocialHistory.objects.get(
        unicode=patient_appointment.unicode)
    functional_history = FunctionalHistory.objects.get(
        unicode=patient_appointment.unicode)
    generay_system = GeneralSystem.objects.get(
        unicode=patient_appointment.unicode)
    skin_problem = SkinProblem.objects.get(unicode=patient_appointment.unicode)
    heent = Heent.objects.get(unicode=patient_appointment.unicode)
    breast = Breast.objects.get(unicode=patient_appointment.unicode)
    pulmonary = Pulmonary.objects.get(unicode=patient_appointment.unicode)
    cardiovascular = Cardiovascular.objects.get(
        unicode=patient_appointment.unicode)
    gastrointestinal = Gastrointestinal.objects.get(
        unicode=patient_appointment.unicode)
    genitourinary = Genitourinary.objects.get(
        unicode=patient_appointment.unicode)
    endocrine = Endocrine.objects.get(unicode=patient_appointment.unicode)
    musculoskeletal = Musculoskeletal.objects.get(
        unicode=patient_appointment.unicode)
    neurologic = Neurologic.objects.get(unicode=patient_appointment.unicode)

    admit = AppointmentForm(instance=patient_appointment)

    context = {
        'title': title,
        'doctor': doctor,
        'is_admin': is_admin,
        'nav_active': nav_active,
        'patient': patient,
        'doctors': doctors,
        'cancel_and_refer_form': cancel_and_refer_form,
        'cancel_appointment_form': cancel_appointment_form,
        'today': today,
        'appointment_date': appointment_date,
        'previous_appointments': previous_appointments,
        'patient_appointment': patient_appointment,
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
def previous(request, pk):
    title = 'Previous Appointment'
    is_admin = request.user.is_superuser
    patient_appointment = Appoinment.objects.get(id=pk)
    patient = patient_appointment.patient
    doctor = request.user.doctor
    chief_complaint = ChiefComplaint.objects.get(
        unicode=patient_appointment.unicode)
    present_illness_image = PresentIllnessImage.objects.get(
        unicode=patient_appointment.unicode)
    present_illness = PresentIllness.objects.get(
        unicode=patient_appointment.unicode)
    childhood_illness = ChildhoodIllness.objects.get(
        unicode=patient_appointment.unicode)
    adult_illness = AdultIllness.objects.get(
        unicode=patient_appointment.unicode)
    history_of_immunization = HistoryOfImmunization.objects.get(
        unicode=patient_appointment.unicode)
    family_history = FamilyHistory.objects.get(
        unicode=patient_appointment.unicode)
    personal_and_social_history = PersonalAndSocialHistory.objects.get(
        unicode=patient_appointment.unicode)
    functional_history = FunctionalHistory.objects.get(
        unicode=patient_appointment.unicode)
    generay_system = GeneralSystem.objects.get(
        unicode=patient_appointment.unicode)
    skin_problem = SkinProblem.objects.get(unicode=patient_appointment.unicode)
    heent = Heent.objects.get(unicode=patient_appointment.unicode)
    breast = Breast.objects.get(unicode=patient_appointment.unicode)
    pulmonary = Pulmonary.objects.get(unicode=patient_appointment.unicode)
    cardiovascular = Cardiovascular.objects.get(
        unicode=patient_appointment.unicode)
    gastrointestinal = Gastrointestinal.objects.get(
        unicode=patient_appointment.unicode)
    genitourinary = Genitourinary.objects.get(
        unicode=patient_appointment.unicode)
    endocrine = Endocrine.objects.get(unicode=patient_appointment.unicode)
    musculoskeletal = Musculoskeletal.objects.get(
        unicode=patient_appointment.unicode)
    neurologic = Neurologic.objects.get(unicode=patient_appointment.unicode)

    admit = AppointmentForm(instance=patient_appointment)

    context = {
        'title': title,
        'doctor': doctor,
        'is_admin': is_admin,
        'patient': patient,
        'patient_appointment': patient_appointment,
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
    return render(request, 'appointments/previous.html', context)


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


@login_required(login_url='login')
def cancelAppointment(request, pk):
    appointment = Appoinment.objects.get(id=pk)
    globe_id = 'aoxpSMBBaetq5cddAbTBnLtKGo87S7nB'
    globe_secret = '073f862eb7f111301c6a6af605626415a67865a477ab4443937844a341b1ade0'
    code = appointment.patient.client.code
    if request.method == 'POST':
        doctor = request.user.doctor
        response = requests.post(
            'https://developer.globelabs.com.ph/oauth/access_token', params={
                'app_id': globe_id,
                'app_secret': globe_secret,
                'code': code
            })
        access_token = response.json()['access_token']
        checkup_date = appointment.checkup_date.strftime('%B %d, %Y')
        checkup_start = appointment.checkup_start.strftime(
            '%I:%M %p')
        checkup_end = appointment.checkup_end.strftime(
            '%I:%M %p')
        message_notes = f"Dr. {doctor.first_name} {doctor.last_name} cancelled your appointment scheduled on { checkup_date } at {checkup_start}-{checkup_end}.\n\nAdditional Message: Dr. {doctor.first_name}  {doctor.last_name} says: \"{request.POST['message']}\""

        body = {
            'outboundSMSMessageRequest': {
                'senderAddress': '3796',
                'outboundSMSTextMessage': {
                    'message': message_notes
                }
            },
            'address': appointment.patient.client.contact,
        }
        print(response.json())
        cancel_response = requests.post(
            'https://devapi.globelabs.com.ph/smsmessaging/v1/outbound/21663796/requests',
            params={
                'access_token': access_token
            },
            json=body,
            headers={
                'Host': 'devapi.globelabs.com.ph'
            })
        appointment.status = 'none'
        appointment.doctor = None
        appointment.checkup_date = None
        appointment.checkup_start = None
        appointment.checkup_end = None
        appointment.save()
        # cancel_response.raise_for_status()
        print(cancel_response.text)
        print(cancel_response.status_code)
        print(cancel_response.url)
    return redirect('dashboard')


@login_required(login_url='login')
def cancelAndReferAppointment(request, pk):
    appointment = Appoinment.objects.get(id=pk)
    globe_id = 'aoxpSMBBaetq5cddAbTBnLtKGo87S7nB'
    globe_secret = '073f862eb7f111301c6a6af605626415a67865a477ab4443937844a341b1ade0'
    code = appointment.patient.client.code
    if request.method == 'POST':
        doctor = request.user.doctor
        doctor_refer = Doctor.objects.get(id=request.POST['doctor'])
        response = requests.post(
            'https://developer.globelabs.com.ph/oauth/access_token', params={
                'app_id': globe_id,
                'app_secret': globe_secret,
                'code': code
            })
        access_token = response.json()['access_token']
        checkup_date = appointment.checkup_date.strftime('%B %d, %Y')
        checkup_start = appointment.checkup_start.strftime(
            '%I:%M %p')
        checkup_end = appointment.checkup_end.strftime(
            '%I:%M %p')
        message_notes = f"Dr. {doctor.first_name} {doctor.last_name} cancelled your appointment that was originally schedule on {checkup_date} at {checkup_start}-{checkup_end} after checking your medical appointment but recommends you to see Dr. {doctor_refer.first_name} {doctor_refer.last_name} of {doctor_refer.specialization.field}. Have a good day!.\n\nAdditional Message: Dr. {doctor.first_name}  {doctor.last_name} says: \"{request.POST['message']}\""

        body = {
            'outboundSMSMessageRequest': {
                'senderAddress': '3796',
                'outboundSMSTextMessage': {
                    'message': message_notes
                }
            },
            'address': appointment.patient.client.contact,
        }
        print(response.json())
        cancel_response = requests.post(
            'https://devapi.globelabs.com.ph/smsmessaging/v1/outbound/21663796/requests',
            params={
                'access_token': access_token
            },
            json=body,
            headers={
                'Host': 'devapi.globelabs.com.ph'
            })
        appointment.status = 'none'
        appointment.doctor = None
        appointment.checkup_date = None
        appointment.checkup_start = None
        appointment.checkup_end = None
        appointment.save()
        # cancel_response.raise_for_status()
        print(cancel_response.text)
        print(cancel_response.status_code)
        print(cancel_response.url)
    return redirect('dashboard')
