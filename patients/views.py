import io
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from . models import Patient
from appointments.models import Appoinment
from datetime import date, datetime
from django.http import FileResponse
from appointments.models import Appoinment
from patients.models import *
from rapha_web import settings

from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import legal
from reportlab.lib.utils import ImageReader
from reportlab.platypus import PageBreak

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


@login_required(login_url='login')
def pdfReport(request, pk):

    # Patient data
    appointment_data = Appoinment.objects.get(id=pk)
    today = date.today()
    patient = appointment_data.patient
    patient_age = today.year - patient.date_of_birth.year - ((today.month, today.day) < (
        patient.date_of_birth.month, patient.date_of_birth.day))
    nav_active = 'nav-active'
    chief_complaint = ChiefComplaint.objects.get(
        unicode=appointment_data.unicode)
    present_illness_image = PresentIllnessImage.objects.get(
        unicode=appointment_data.unicode)
    present_illness = PresentIllness.objects.get(
        unicode=appointment_data.unicode)
    childhood_illness = ChildhoodIllness.objects.get(
        unicode=appointment_data.unicode)
    adult_illness = AdultIllness.objects.get(
        unicode=appointment_data.unicode)
    history_of_immunization = HistoryOfImmunization.objects.get(
        unicode=appointment_data.unicode)
    family_history = FamilyHistory.objects.get(
        unicode=appointment_data.unicode)
    personal_and_social_history = PersonalAndSocialHistory.objects.get(
        unicode=appointment_data.unicode)
    functional_history = FunctionalHistory.objects.get(
        unicode=appointment_data.unicode)
    general_system = GeneralSystem.objects.get(
        unicode=appointment_data.unicode)
    skin_problem = SkinProblem.objects.get(unicode=appointment_data.unicode)
    heent = Heent.objects.get(unicode=appointment_data.unicode)
    breast = Breast.objects.get(unicode=appointment_data.unicode)
    pulmonary = Pulmonary.objects.get(unicode=appointment_data.unicode)
    cardiovascular = Cardiovascular.objects.get(
        unicode=appointment_data.unicode)
    gastrointestinal = Gastrointestinal.objects.get(
        unicode=appointment_data.unicode)
    genitourinary = Genitourinary.objects.get(
        unicode=appointment_data.unicode)
    gynecologic = Gynecologic.objects.get(
        unicode=appointment_data.unicode)
    endocrine = Endocrine.objects.get(unicode=appointment_data.unicode)
    musculoskeletal = Musculoskeletal.objects.get(
        unicode=appointment_data.unicode)
    neurologic = Neurologic.objects.get(unicode=appointment_data.unicode)


    # Pdf images
    illnes_image = settings.STATIC_URL + present_illness_image.illness_image.url
    rapha_logo = settings.STATIC_URL + 'img/rapha_logo_intact.png'

    img = ImageReader(illnes_image)
    img_width, img_height = img.getSize()

    lines = ['']
    lines = ['']

    # Patient Info
    patient_info = [
      'Patient Info',
      '• Sex: ' + patient.sex,
      '• Birthday: ' + str(patient.date_of_birth),
      '• Age: ' + str(patient_age),
      ''
    ]
    lines.extend(patient_info)

    # Chief Complaint
    chief_complaint_entries = '• '
    chief_complaint_others = ''
    chief_complaints = ['Chief Complaints']
    if chief_complaint.cough:
      chief_complaint_entries = chief_complaint_entries + ' Cough, '
    if chief_complaint.pain:
      chief_complaint_entries = chief_complaint_entries + ' Pain, '
    if chief_complaint.weakness:
      chief_complaint_entries = chief_complaint_entries + ' Weakness, '
    if chief_complaint.decrease_sensation:
      chief_complaint_entries = chief_complaint_entries + ' Decrease sensation, '
    if chief_complaint.rashes:
      chief_complaint_entries = chief_complaint_entries + ' Rashes, '
    if chief_complaint.trouble_breathing:
      chief_complaint_entries = chief_complaint_entries + ' Trouble breathing, '
    if chief_complaint.vomitting:
      chief_complaint_entries = chief_complaint_entries + ' Vomitting, '
    if chief_complaint.voweling:
      chief_complaint_entries = chief_complaint_entries + ' Vowelling, '
    if chief_complaint.others != '' and chief_complaint.others != None :
      chief_complaint_others = '• ' + chief_complaint.others
    chief_complaint_entries = chief_complaint_entries[:-2]
    chief_complaints.append(chief_complaint_entries)
    chief_complaints.append(chief_complaint_others)
    chief_complaints.append('')
    lines.extend(chief_complaints)

    # Present Illness
    present_illness_entries = '• '
    present_illnesses = ['Present Illness']
    if present_illness.symptoms_started != '':
      present_illnesses.append('• Symptoms started: ' + str(present_illness.symptoms_started))
    if present_illness.how_often != '':
      present_illnesses.append('• How often: ' + present_illness.how_often)
    if present_illness.how_long != '':
      present_illnesses.append('• How long: ' + present_illness.how_long)
    if present_illness.describe != '':
      present_illnesses.append('• Description: ' + present_illness.describe)
    if present_illness.severity != '':
      present_illnesses.append('• Severity: ' + str(present_illness.severity))
    if present_illness.affects_walking or present_illness.affects_bathing or present_illness.affects_dressing or present_illness.affects_eating or present_illness.affects_hygiene or present_illness.affects_sleeping or present_illness.affects_toilet or present_illness.affects_sex or present_illness.affects_bowel or present_illness.affects_urination:
      if present_illness.affects_walking:
        present_illness_entries = present_illness_entries + ' Walking, '
      if present_illness.affects_bathing:
        present_illness_entries = present_illness_entries + ' Bathing, '
      if present_illness.affects_dressing:
        present_illness_entries = present_illness_entries + ' Dressing, '
      if present_illness.affects_eating:
        present_illness_entries = present_illness_entries + ' Eating, '
      if present_illness.affects_hygiene:
        present_illness_entries = present_illness_entries + ' Hygiene, '
      if present_illness.affects_sleeping:
        present_illness_entries = present_illness_entries + ' Sleeping, '
      if present_illness.affects_toilet:
        present_illness_entries = present_illness_entries + ' Toilet, '
      if present_illness.affects_sex:
        present_illness_entries = present_illness_entries + ' Sex, '
      if present_illness.affects_bowel:
        present_illness_entries = present_illness_entries + ' Bowel, '
      if present_illness.affects_urination:
        present_illness_entries = present_illness_entries + ' Urination, '
      present_illness_entries = present_illness_entries[:-2]
      present_illnesses.append('Affeted daily living activites')
      present_illnesses.append(present_illness_entries)

    if present_illness.affects_activities != None and present_illness.affects_activities != '':
      present_illnesses.append('• Affected activities: ' + present_illness.affects_activities)
    if present_illness.activities_worse != '' and present_illness.activities_worse != None:
      present_illnesses.append(
          '• Activities making it worse: ' + present_illness.activities_worse)
    if present_illness.activities_improves != '' and present_illness.activities_improves != None:
      present_illnesses.append(
          '• Activities improving the condition: ' + present_illness.activities_improves)
    if present_illness.other_symptoms != '' and present_illness.other_symptoms != None:
      present_illnesses.append(
          '• Other symptoms: ' + present_illness.other_symptoms)
    if present_illness.medications != '' and present_illness.medications != None:
      present_illnesses.append(
          '• Current medications: ' + present_illness.medications)
    present_illnesses.append('')
    lines.extend(present_illnesses)

    # Childhood Illness
    childhood_illness_entries = '• '
    childhood_illnesses = ['Childhood Illness']
    if childhood_illness.measles or childhood_illness.mumps or childhood_illness.rubella or childhood_illness.asthma or childhood_illness.primary_complex or childhood_illness.chicken_pox or (childhood_illness.others != '' and childhood_illness.others != None):
      if childhood_illness.measles:
        childhood_illness_entries = childhood_illness_entries + ' Measles, '
      if childhood_illness.mumps:
        childhood_illness_entries = childhood_illness_entries + ' Mumpms, '
      if childhood_illness.rubella:
        childhood_illness_entries = childhood_illness_entries + ' Rubella, '
      if childhood_illness.asthma:
        childhood_illness_entries = childhood_illness_entries + ' Asthma, '
      if childhood_illness.primary_complex:
        childhood_illness_entries = childhood_illness_entries + ' Primary complex, '
      if childhood_illness.chicken_pox:
        childhood_illness_entries = childhood_illness_entries + ' Chicken pox, '
      childhood_illness_entries = childhood_illness_entries[:-2]
      childhood_illnesses.append(childhood_illness_entries)
      if childhood_illness.others != '' and childhood_illness.others != None:
        childhood_illnesses.append('• Others: ' + childhood_illness.others)
      childhood_illnesses.append('')
      lines.extend(childhood_illnesses)

    # Adult Illness
    adult_illness_entries = '• '
    adult_illnesses = ['Adult Illness']
    if adult_illness.diabetes or adult_illness.hypertension or adult_illness.stroke or adult_illness.arthritis or adult_illness.tuberculosis or adult_illness.heart_disease or adult_illness.thyroid or adult_illness.asthma or (adult_illness.others != '' and adult_illness.others != None):
      if adult_illness.diabetes:
        adult_illness_entries = adult_illness_entries + ' Diabetes, '
      if adult_illness.hypertension:
        adult_illness_entries = adult_illness_entries + ' Hypertension, '
      if adult_illness.stroke:
        adult_illness_entries = adult_illness_entries + ' Stroke, '
      if adult_illness.arthritis:
        adult_illness_entries = adult_illness_entries + ' Arthritis, '
      if adult_illness.tuberculosis:
        adult_illness_entries = adult_illness_entries + ' Tuberculosis, '
      if adult_illness.heart_disease:
        adult_illness_entries = adult_illness_entries + ' Heart_disease, '
      if adult_illness.thyroid:
        adult_illness_entries = adult_illness_entries + ' Thyroid, '
      if adult_illness.asthma:
        adult_illness_entries = adult_illness_entries + ' Asthma, '
        adult_illness_entries = adult_illness_entries[:-2]
        adult_illnesses.append(adult_illness_entries)
      if adult_illness.others != '' and adult_illness.others != None:
        adult_illnesses.append('• Others: ' + adult_illness.others)
      adult_illnesses.append('')
      lines.extend(adult_illnesses)

    # History of Immunization
    history_of_immunizations = ['Surgeries, Hospitalizations & Immunization']
    immunizations_entries = '• '
    tests_entries = '• '
    if history_of_immunization.surgeries != '' and history_of_immunization.surgeries != None:
      history_of_immunizations.append(
          '• Past Hospitalizations: ' + history_of_immunization.surgeries)
    if history_of_immunization.medical_allergies != '' and history_of_immunization.medical_allergies != None:
      history_of_immunizations.append(
          '• Past Surgeries: ' + history_of_immunization.medical_allergies)
    if history_of_immunization.hepatitis_a or history_of_immunization.hepatitis_b or history_of_immunization.polio or history_of_immunization.measles or history_of_immunization.influenza or history_of_immunization.varicella or history_of_immunization.influenza_b or history_of_immunization.pneumococcal or history_of_immunization.meningococcal or history_of_immunization.hpv or history_of_immunization.others_immunization != '':
      history_of_immunizations.append('History of Immunization')
      if history_of_immunization.hepatitis_a:
        immunizations_entries = immunizations_entries + ' Hepatitis A, '
      if history_of_immunization.hepatitis_b:
        immunizations_entries = immunizations_entries +' Hepatitis B, '
      if history_of_immunization.polio:
        immunizations_entries = immunizations_entries  + ' Polio, '
      if history_of_immunization.measles:
        immunizations_entries = immunizations_entries +' Measles, '
      if history_of_immunization.influenza:
        immunizations_entries = immunizations_entries + ' Influenza, '
      if history_of_immunization.varicella:
        immunizations_entries = immunizations_entries + ' Varicella, '
      if history_of_immunization.influenza_b:
        immunizations_entries = immunizations_entries + ' Influenza B, '
      if history_of_immunization.pneumococcal:
        immunizations_entries = immunizations_entries + ' Pneumococcal, '
      if history_of_immunization.meningococcal:
        immunizations_entries = immunizations_entries + ' Meningococcal, '
      if history_of_immunization.hpv:
        immunizations_entries = immunizations_entries + ' HPV, '
      immunizations_entries = immunizations_entries[:-2]
      history_of_immunizations.append(immunizations_entries)
      if history_of_immunization.others_immunization != None:
        history_of_immunizations.append(
            '• Others: ' + history_of_immunization.others_immunization)
    if history_of_immunization.tuberculosis_test or history_of_immunization.stool_test or history_of_immunization.colonoscopy or history_of_immunization.blood_test or history_of_immunization.x_ray or history_of_immunization.ct_scan_ultrasound or history_of_immunization.pap_smears or history_of_immunization.mammograms or history_of_immunization.others_test:
      history_of_immunizations.append('Underwent Tests')
      if history_of_immunization.tuberculosis_test:
        tests_entries = tests_entries + ' Tuberculosis test, '
      if history_of_immunization.stool_test:
        tests_entries = tests_entries + ' Stool test, '
      if history_of_immunization.colonoscopy:
        tests_entries = tests_entries + ' Colonoscopy, '
      if history_of_immunization.blood_test:
        tests_entries = tests_entries + ' Blood_test, '
      if history_of_immunization.x_ray:
        tests_entries = tests_entries + ' X-ray, '
      if history_of_immunization.ct_scan_ultrasound:
        tests_entries = tests_entries + ' CT Scan/Ultrasound, '
      if history_of_immunization.pap_smears:
        tests_entries = tests_entries + ' Pap smears, '
      if history_of_immunization.mammograms:
        tests_entries = tests_entries + ' Mammograms, '
      if tests_entries != '• ':
        tests_entries = tests_entries[:-2]
        history_of_immunizations.append(tests_entries)
      if history_of_immunization.others_test != '' and history_of_immunization.others_test != None:
        history_of_immunizations.append(
            '• Others: ' + history_of_immunization.others_test)
      history_of_immunizations.append('')
    lines.extend(history_of_immunizations)

    # Family History
    family_histories_entries = '• '
    family_histories = ['Family History']
    if family_history.diabetes or family_history.hypertension or family_history.stroke or family_history.arthritis or family_history.tuberculosis or family_history.heart_disease or family_history.thyroid or family_history.asthma or family_history.others != '':
      if family_history.diabetes:
        family_histories_entries = family_histories_entries + ' Diabetes, '
      if family_history.hypertension:
        family_histories_entries = family_histories_entries + ' Hypertension, '
      if family_history.stroke:
        family_histories_entries = family_histories_entries + ' Stroke, '
      if family_history.arthritis:
        family_histories_entries = family_histories_entries + ' Arthritis, '
      if family_history.tuberculosis:
        family_histories_entries = family_histories_entries + ' Tuberculosis, '
      if family_history.heart_disease:
        family_histories_entries = family_histories_entries + ' Heart disease, '
      if family_history.thyroid:
        family_histories_entries = family_histories_entries + ' Thyroid, '
      if family_histories_entries != '• ':
        family_histories_entries = family_histories_entries[:-2]
      family_histories.append(family_histories_entries)
      if family_history.others != '' and family_history.others != None:
        family_histories.append('• Others: ' + family_history.others)
      family_histories.append('')
      lines.extend(family_histories)

    # Personal and Social History
    personal_and_social_histories = ['Personal and Social History']
    if personal_and_social_history.physical_activity != '' and personal_and_social_history.physical_activity != None:
      personal_and_social_histories.append(
          '• Physical Activities: ' + personal_and_social_history.physical_activity)
    if personal_and_social_history.healthy_foods != '' and personal_and_social_history.healthy_foods != None:
      personal_and_social_histories.append(
          '• Healthy Foods: ' + personal_and_social_history.healthy_foods)
    if personal_and_social_history.course_year_level != '' and personal_and_social_history.course_year_level != None:
      personal_and_social_histories.append(
          '• Course/Year Level: ' + personal_and_social_history.course_year_level)
    if personal_and_social_history.occupation != '' and personal_and_social_history.occupation != None:
      personal_and_social_histories.append(
          '• Occupation: ' + personal_and_social_history.occupation)
    if personal_and_social_history.sticks_per_day != '' and personal_and_social_history.sticks_per_day != None:
      personal_and_social_histories.append(
          '• Smoking: Yes, ' + personal_and_social_history.sticks_per_day + ' stick(s) per day')
    if personal_and_social_history.years_smoking != '' and personal_and_social_history.years_smoking != None:
      personal_and_social_histories.append(
          '• Years smoking: ' + personal_and_social_history.years_smoking + ' year(s)')
    if personal_and_social_history.when_stop_smoking != '' and personal_and_social_history.when_stop_smoking != None:
      personal_and_social_histories.append(
          '• Stopped on: ' + personal_and_social_history.when_stop_smoking)
    if personal_and_social_history.bottles_per_day != '' and personal_and_social_history.bottles_per_day != None:
      personal_and_social_histories.append(
          '• Drinking: Yes, ' + personal_and_social_history.bottles_per_day + ' bottle(s) per day')
    if personal_and_social_history.how_often_drinking != '' and personal_and_social_history.how_often_drinking != None:
      personal_and_social_histories.append(
          '• How often: Yes, ' + personal_and_social_history.how_often_drinking)
    if (personal_and_social_history.substance_drugs != '' and personal_and_social_history.substance_drugs != None)  or (personal_and_social_history.when_drugs_used != '' and personal_and_social_history.when_drugs_used != None)  or (personal_and_social_history.how_often_drugs != '' and personal_and_social_history.how_often_drugs != None) or (personal_and_social_history.last_time_drugs != '' and personal_and_social_history.last_time_drugs != None):
      personal_and_social_histories.append('History of Illegal Drugs')
      if personal_and_social_history.substance_drugs != '' and personal_and_social_history.substance_drugs != None:
        personal_and_social_histories.append(
            '• Substance: ' + personal_and_social_history.substance_drugs)
      if personal_and_social_history.when_drugs_used != '' and personal_and_social_history.when_drugs_used != None:
        personal_and_social_histories.append(
            '• Started using: ' + personal_and_social_history.when_drugs_used)
      if personal_and_social_history.how_often_drugs != '' and personal_and_social_history.how_often_drugs != None:
        personal_and_social_histories.append(
            '• How often: ' + personal_and_social_history.how_often_drugs)
      if personal_and_social_history.last_time_drugs != '' and personal_and_social_history.last_time_drugs != None:
        personal_and_social_histories.append(
            '• Last usage: ' + personal_and_social_history.last_time_drugs)
    personal_and_social_histories.append('')
    lines.extend(personal_and_social_histories)

    # Functional History
    if (functional_history.assistive_walking != '' and functional_history.assistive_walking != None) or functional_history.affects_walking or functional_history.affects_bathing or functional_history.affects_dressing or functional_history.affects_eating or functional_history.affects_hygiene or functional_history.affects_sleeping or functional_history.affects_toilet or functional_history.affects_sex or functional_history.affects_bowel or functional_history.affects_urination or (functional_history.needs_support == '' and functional_history.needs_support == None) or (functional_history.assistive_devices != '' and functional_history.assistive_devices != None) or (functional_history.difficulties_activities != '' and functional_history.difficulties_activities != None) or (functional_history.difficulties_assistance != '' and functional_history.difficulties_assistance != None) or (functional_history.difficulties_in_complicated != '' and functional_history.difficulties_in_complicated != None) or (functional_history.difficulties_in_verbal != '' and functional_history.difficulties_in_verbal != None):
      functional_history_entries = '• '
      functional_histories = ['Functional History']
      if functional_history.assistive_walking != None:
        functional_histories.append(
            '• Assistive device in walking: ' + functional_history.assistive_walking)
      if functional_history.affects_walking or functional_history.affects_bathing or functional_history.affects_dressing or functional_history.affects_eating or functional_history.affects_hygiene or functional_history.affects_sleeping or functional_history.affects_toilet or functional_history.affects_sex or functional_history.affects_bowel or functional_history.affects_urination:
        if functional_history.affects_walking:
          functional_history_entries = functional_history_entries + ' Walking, '
        if functional_history.affects_bathing:
          functional_history_entries = functional_history_entries + ' Bathing, '
        if functional_history.affects_dressing:
          functional_history_entries = functional_history_entries + ' Dressing, '
        if functional_history.affects_eating:
          functional_history_entries = functional_history_entries + ' Eating, '
        if functional_history.affects_hygiene:
          functional_history_entries = functional_history_entries + ' Hygiene, '
        if functional_history.affects_sleeping:
          functional_history_entries = functional_history_entries + ' Sleeping, '
        if functional_history.affects_toilet:
          functional_history_entries = functional_history_entries + ' Toilet, '
        if functional_history.affects_sex:
          functional_history_entries = functional_history_entries + ' Sex, '
        if functional_history.affects_bowel:
          functional_history_entries = functional_history_entries + ' Bowel, '
        if functional_history.affects_urination:
          functional_history_entries = functional_history_entries + ' Urination, '
        if functional_history_entries != '• ':
          functional_histories.append(
              'Daily living activities that you have difficulties with')
          functional_histories.append(functional_history_entries)
        functional_history_entries = functional_history_entries[:-2]
      if functional_history.needs_support != '' and functional_history.needs_support != None:
        functional_histories.append(
            '• How much support do you need: ' + functional_history.needs_support)
      if functional_history.assistive_devices != '' and functional_history.assistive_devices != None:
        functional_histories.append(
            '• Assistive devices: ' + functional_history.assistive_devices)
      if functional_history.difficulties_activities != '' and functional_history.difficulties_activities != None:
        functional_histories.append(
            'Activities you have difficulties with: ' + functional_history.difficulties_activities)
      if functional_history.difficulties_assistance != '' and functional_history.difficulties_assistance != None:
        functional_histories.append(
            '• Description: ' + functional_history.difficulties_assistance)
      if functional_history.difficulties_in_complicated != '' and functional_history.difficulties_in_complicated != None:
        functional_histories.append(
            '• Complicated activites: ' + functional_history.difficulties_in_complicated)
      if functional_history.difficulties_in_verbal != '' and functional_history.difficulties_in_verbal != None:
        functional_histories.append(
            '• Communication: ' + functional_history.difficulties_in_verbal)
      functional_histories.append('')
      lines.extend(functional_histories)

      # Review of Systems
      lines.append('Review of Systems')

      # General system
      general_system_entries = ''
      general_systems = []

      if general_system.fever or general_system.fatigue or  general_system.weight_change or  general_system.weakness: 
        general_system_entries = '• '
        if general_system.fever:
          general_system_entries = general_system_entries + ' Fever, '
        if general_system.fatigue:
          general_system_entries = general_system_entries + ' Fatigue, '
        if general_system.weight_change:
          general_system_entries = general_system_entries + ' Weight change, '
        if general_system.weakness:
          general_system_entries = general_system_entries + ' Weakness, '
        general_system_entries = general_system_entries[:-2]
        general_systems.append(general_system_entries)
        general_systems.append('')
        lines.extend(general_systems)

      # Skin problems
      skin_problem_entries = '• '
      skin_problems = ['Skin Problems']
      if not skin_problem.none:
        if skin_problem.rashes:
          skin_problem_entries = skin_problem_entries + ' Rashes, '
        if skin_problem.lumps:
          skin_problem_entries = skin_problem_entries + ' Lumps, '
        if skin_problem.sores:
          skin_problem_entries = skin_problem_entries + ' Sores, '
        if skin_problem.itching:
          skin_problem_entries = skin_problem_entries + ' Itching, '
        if skin_problem.dryness:
          skin_problem_entries = skin_problem_entries + ' Dryness, '
        if skin_problem.changes_in_color:
          skin_problem_entries = skin_problem_entries + ' Changes in color, '
        if skin_problem.changes_in_hair_nails:
          skin_problem_entries = skin_problem_entries + ' changes in hair/nails, '
        skin_problem_entries = skin_problem_entries[:-2]
        skin_problems.append(skin_problem_entries)
        skin_problems.append('')
        lines.extend(skin_problems)

      # Heent
      heent_entries = '• '
      heents = ['Head Eyes Ears Nose Throat']
      if not heent.none:
        if heent.headache:
          heent_entries = heent_entries + ' Headache, '
        if heent.dizziness:
          heent_entries = heent_entries + ' Dizziness, '
        if heent.lightheadedness:
          heent_entries = heent_entries + ' Lightheadedness, '
        if heent.changes_in_vision:
          heent_entries = heent_entries + ' Changes in vision, '
        if heent.eye_pain:
          heent_entries = heent_entries + ' Eye pain, '
        if heent.eye_redness:
          heent_entries = heent_entries + ' Eye redness, '
        if heent.double_vision:
          heent_entries = heent_entries + ' Double vision, '
        if heent.watery_eyes:
          heent_entries = heent_entries + ' Watery eyes, '
        if heent.poor_hearing:
          heent_entries = heent_entries + ' Poor hearing, '
        if heent.ringing_ears:
          heent_entries = heent_entries + ' Ringing ears, '
        if heent.ear_discharge:
          heent_entries = heent_entries + ' Ear discharge, '
        if heent.stuffy_nose:
          heent_entries = heent_entries + ' Stuffy nose, '
        if heent.nasal_discharge:
          heent_entries = heent_entries + ' Nasal discharge, '
        if heent.nasal_bleeding:
          heent_entries = heent_entries + ' Nasal bleeding, '
        if heent.unusual_odors:
          heent_entries = heent_entries + ' Unusual odors, '
        if heent.mouth_sores:
          heent_entries = heent_entries + ' Mouth sores, '
        if heent.altered_taste:
          heent_entries = heent_entries + ' Altered taste, '
        if heent.sore_tongue:
          heent_entries = heent_entries + ' Sore tongue, '
        if heent.gum_problem:
          heent_entries = heent_entries + ' Gum problem, '
        if heent.sore_throat:
          heent_entries = heent_entries + ' Sore throat, '
        if heent.hoarseness:
          heent_entries = heent_entries + ' Hoarseness, '
        if heent.swelling:
          heent_entries = heent_entries + ' Swelling, '
        if heent.diffuculty_swallowing:
          heent_entries = heent_entries + ' Diffuculty swallowing, '
        heent_entries = heent_entries[:-2]
        heents.append(heent_entries)
        heents.append('')
        lines.extend(heents)
      
      #Breast
      breast_entries = '• '
      breasts = ['Breast']
      if not breast:
        if breast.breast_lumps:
          breast_entries = breast_entries + ' Breast lumps, '
        if breast.nipple_discharge:
          breast_entries = breast_entries + ' Nipple discharge, '
        if breast.bleeding:
          breast_entries = breast_entries + ' Bleeding, '
        if breast.breast_swelling:
          breast_entries = breast_entries + ' Breast swelling, '
        if breast.breast_tenderness:
          breast_entries = breast_entries + ' Breast tenderness, '
        breast_entries = breast_entries[:-2]
        breasts.append(breast_entries)
        breasts.append('')
        lines.extend(breasts)

      # Pulmonary
      pulmonary_entries = '• '
      pulmonaries = ['Pulmonary']
      if not pulmonary.none:
        if pulmonary.cough:
          pulmonary_entries = pulmonary_entries + ' Cough, '
        if pulmonary.sputum:
          pulmonary_entries = pulmonary_entries + ' Sputum, '
        if pulmonary.bloody_sputum:
          pulmonary_entries = pulmonary_entries + ' Bloody sputum, '
        if pulmonary.chest_pain:
          pulmonary_entries = pulmonary_entries + ' Chest pain, '
        if pulmonary.shortness_breath:
          pulmonary_entries = pulmonary_entries + ' Shortness breath, '
        pulmonary_entries = pulmonary_entries[:-2]
        pulmonaries.append(pulmonary_entries)
        pulmonaries.append('')
        lines.extend(pulmonaries)

      # Cardiovascular
      cardiovascular_entries = '• '
      cardiovasculars = ['Cardiovascular']
      if not cardiovascular.none:
        if cardiovascular.chest_pain:
          cardiovascular_entries = cardiovascular_entries + ' Chest pain, '
        if cardiovascular.shortness_of_breath:
          cardiovascular_entries = cardiovascular_entries + ' Shortness of breath, '
        if cardiovascular.palpitations:
          cardiovascular_entries = cardiovascular_entries + ' Palpitations, '
        if cardiovascular.cough:
          cardiovascular_entries = cardiovascular_entries + ' Cough, '
        if cardiovascular.swelling_of_ankles:
          cardiovascular_entries = cardiovascular_entries + ' Swelling of ankles, '
        if cardiovascular.trouble_lying:
          cardiovascular_entries = cardiovascular_entries + ' Trouble lying, '
        if cardiovascular.fatigue:
          cardiovascular_entries = cardiovascular_entries + ' Fatigue, '
        cardiovascular_entries = cardiovascular_entries[:-2]
        cardiovasculars.append(cardiovascular_entries)
        cardiovasculars.append('')
        lines.extend(cardiovasculars)

      # Gastrointestinal
      gastrointestinal_entries = '• '
      gastrointestinals = ['Gastrointestinal']
      if not gastrointestinal.none:
        if gastrointestinal.changes_in_appetite:
          gastrointestinal_entries = gastrointestinal_entries + ' Changes in appetite, '
        if gastrointestinal.nausea:
          gastrointestinal_entries = gastrointestinal_entries + ' Nausea, '
        if gastrointestinal.vomitting:
          gastrointestinal_entries = gastrointestinal_entries + ' Vomitting, '
        if gastrointestinal.diarrhea:
          gastrointestinal_entries = gastrointestinal_entries + ' Diarrhea, '
        if gastrointestinal.constipation:
          gastrointestinal_entries = gastrointestinal_entries + ' Constipation, '
        if gastrointestinal.changes_in_bowel:
          gastrointestinal_entries = gastrointestinal_entries + ' Changes in bowel, '
        if gastrointestinal.bleeding_rectum:
          gastrointestinal_entries = gastrointestinal_entries + ' Bleeding rectum, '
        if gastrointestinal.hemorrhoids:
          gastrointestinal_entries = gastrointestinal_entries + ' Hemorrhoids, '
        if gastrointestinal.decreased_stool:
          gastrointestinal_entries = gastrointestinal_entries + ' Decreased stool, '
        gastrointestinal_entries = gastrointestinal_entries[:-2]
        gastrointestinals.append(gastrointestinal_entries)
        gastrointestinals.append('')
        lines.extend(gastrointestinals)

        # Genitourinary
        genitourinary_entries = '• '
        genitourinaries = ['Genitourinary']
        if not genitourinary.none:
          if genitourinary.painful_urination:
            genitourinary_entries = genitourinary_entries + ' Painful urination'
          if genitourinary.increased_decreased_frequency:
            genitourinary_entries = genitourinary_entries + ' Increased/decreased frequency'
          if genitourinary.bloody_urine:
            genitourinary_entries = genitourinary_entries + ' Bloody urine'
          if genitourinary.trouble_urination:
            genitourinary_entries = genitourinary_entries + ' Trouble urination'
          genitourinary_entries = genitourinary_entries[:-2]
          genitourinaries.append(genitourinary_entries)
          genitourinaries.append('')
          lines.extend(genitourinaries)

        # Gynecologic
        gynecologic_entries = '• Others'
        gynecologics = ['Gynecologic']
        if (gynecologic.pregnancies != '' and gynecologic.pregnancies != None) or (gynecologic.miscarriages != '' and gynecologic.miscarriages != None) or (gynecologic.last_period != '' and gynecologic.last_period != None) or not gynecologic.none:
          if gynecologic.pregnancies != '' and gynecologic.pregnancies != None:
            gynecologics.append('• Pregnancies: ' + gynecologic.pregnancies)
          if gynecologic.miscarriages != '' and gynecologic.miscarriages != None:
            gynecologics.append('• Miscarriages: ' + gynecologic.miscarriages)
          if gynecologic.last_period != '' and gynecologic.last_period != None:
            gynecologics.append('• Last period: ' + gynecologic.last_period)
          if not gynecologic.none:
            if gynecologic.irregular_menstration:
              gynecologic_entries = gynecologic_entries + ' Irregular menstration, '
            if gynecologic.vaginal_bleeding:
              gynecologic_entries = gynecologic_entries + ' Vaginal bleeding, '
            if gynecologic.cessation_of_periods:
              gynecologic_entries = gynecologic_entries + ' Cessation of periods, '
            if gynecologic.hot_flashes:
              gynecologic_entries = gynecologic_entries + ' Hot flashes, '
            if gynecologic.vaginal_itching:
              gynecologic_entries = gynecologic_entries + ' Vaginal itching, '
            if gynecologic.sexual_dysfunction:
              gynecologic_entries = gynecologic_entries + ' Sexual dysfunction, '
            gynecologic_entries = gynecologic_entries[:-2]
            gynecologics.append(gynecologic_entries)
          gynecologics.append('')
          lines.extend(gynecologics)

        #  Endocrine
        endocrine_entries = '• '
        endocrines = ['Endocrine']
        if not endocrine.none:
          if endocrine.hot_or_cold:
            endocrine_entries = endocrine_entries + ' Hot or cold, '
          if endocrine.fatigue:
            endocrine_entries = endocrine_entries + ' Hot_or_cold, '
          if endocrine.changes_hair_skin:
            endocrine_entries = endocrine_entries + ' Changes in hair/skin, '
          if endocrine.shaking:
            endocrine_entries = endocrine_entries + ' Shaking, '
          endocrine_entries = endocrine_entries[:-2]
          endocrines.append(endocrine_entries)
          endocrines.append('')
          lines.extend(endocrines)

        # Musculoskeletal
        musculoskeletal_entries = '• '
        musculoskeletals = ['Musculoskeletal']
        if not musculoskeletal.none:
          if musculoskeletal.joints_muscle_pain:
            musculoskeletal_entries = musculoskeletal_entries + ' Joints/muscle pain, '
          if musculoskeletal.stiffness:
            musculoskeletal_entries = musculoskeletal_entries + ' Stiffness, '
          if musculoskeletal.motion_limitation:
            musculoskeletal_entries = musculoskeletal_entries + ' Motion limitation, '
          if musculoskeletal.muscle_atrophy:
            musculoskeletal_entries = musculoskeletal_entries + ' Muscle atrophy, '
          if musculoskeletal.muscle_hypertrophy:
            musculoskeletal_entries = musculoskeletal_entries + ' Muscle hypertrophy, '
          musculoskeletal_entries = musculoskeletal_entries[:-2]
          musculoskeletals.append(musculoskeletal_entries)
          musculoskeletals.append('')
          lines.extend(musculoskeletals)




    # PDF GENERATION REPORT
    # PDF report file name
    document_filename = appointment_data.unicode + '.pdf'

    # Create bytestream buffer
    buffer = io.BytesIO()

    # Create a canvas
    pdf_canvas = canvas.Canvas(buffer, pagesize=legal, bottomup=0)

    pdf_canvas.setTitle('Patient PDF Report')
    pdf_canvas.saveState()
    pdf_canvas.translate(100, 100)
    pdf_canvas.scale(1, -1)
    pdf_canvas.drawImage(illnes_image, 330, -220,
                         height=img_height*0.15, width=img_width*0.15, mask='auto')
    pdf_canvas.drawImage(rapha_logo, 165, 30, height=44, width=100, mask='auto')
    pdf_canvas.restoreState()

    # Create a text object
    text_object = pdf_canvas.beginText()
    text_object.setTextOrigin(inch, inch)
    text_object.setFont('Helvetica', 10)

    # Loop
    for line in lines:
      if line == 'Patient Info' or line == 'Chief Complaints' or line == 'Present Illness' or line == 'Childhood Illness' or line == 'Adult Illness' or line == 'Surgeries, Hospitalizations & Immunization' or line == 'Family History' or line == 'Personal and Social History' or line == 'Functional History' or line == 'Review of Systems' or line == 'General System' or line == 'Skin Problems' or line == 'Head Eyes Ears Nose Throat' or line == 'Breasts' or line == 'Pulmonary' or line == 'Cardiovascular' or line == 'Gynecologic' or line == 'Endocrine' or line == 'Musculoskeletal':
        text_object.setFont('Helvetica-Bold', 11)
      elif line == 'Affeted daily living activites' or line == 'History of Immunization' or line == 'Underwent Tests' or line == 'Daily living activities that you have difficulties with' or line == 'History of Illegal Drugs':
        text_object.setFont('Helvetica-Bold', 10)
      else:
        text_object.setFont('Helvetica', 10)

      text_object.textLine(line)


    pdf_canvas.drawText(text_object)
    pdf_canvas.showPage()

    
    # Second Page
    # pdf_canvas.saveState()
    # pdf_canvas.translate(100, 100)
    # pdf_canvas.scale(1, -1)
    # pdf_canvas.drawImage(rapha_logo, 165, 30, height=44, width=100, mask='auto')
    # pdf_canvas.restoreState()

    # text_object = pdf_canvas.beginText(inch, 10*inch)
    # text_object.setFont('Helvetica', 10)

    # # Loop
    # for second_line in lines:
      # if line == 'General System' or line == 'Skin Problems' or line == 'Heent' or line == 'Breasts' or line == 'Pulmonary' or line == 'Cardiovascular' or line == 'Gynecologic' or line == 'Endocrine' or line == 'Musculoskeletal':
    #     text_object.setFont('Helvetica-Bold', 11)
    #   else:
    #     text_object.setFont('Helvetica', 10)
    #   text_object.textLine(second_line)

    # pdf_canvas.showPage()
    pdf_canvas.save()
    buffer.seek(0)

    return FileResponse(buffer, as_attachment=True, filename=document_filename)
