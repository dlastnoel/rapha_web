from datetime import datetime
from pydoc import describe
from pyexpat import model
from random import choice
import uuid
from django.db import models
from clients.models import Client
# from doctors.models import Doctor

# Create your models here.


class Patient(models.Model):
    SEX = (
        ('male', 'Male'),
        ('female', 'Female'),
    )
    MARITAL_STATUS = (
        ('single', 'Single'),
        ('married', 'Married'),
        ('separated', 'Separated'),
        ('widowed', 'Widowed'),
    )
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)
    client = models.ForeignKey(
        Client, on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True)
    sex = models.CharField(max_length=50, choices=SEX)
    marital_status = models.CharField(max_length=50, choices=MARITAL_STATUS)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        if self.client.username is not None:
            return self.client.username


class ChiefComplaint(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    unicode = models.CharField(max_length=300, null=True)
    cough = models.BooleanField()
    pain = models.BooleanField()
    weakness = models.BooleanField()
    decrease_sensation = models.BooleanField()
    rashes = models.BooleanField()
    trouble_breathing = models.BooleanField()
    vomitting = models.BooleanField()
    voweling = models.BooleanField()
    others = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)


class PresentIllnessImage(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    unicode = models.CharField(max_length=300, null=True)
    illness_image = models.ImageField(
        null=True, blank=True, upload_to='illnesses/')
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)


class PresentIllness(models.Model):
    SEVERITY = (
        ('mild', 'Mild'),
        ('moderate', 'Moderate'),
        ('severe', 'Severe')
    )
    patient = models.ForeignKey(
        Patient, on_delete=models.CASCADE, null=True, blank=True)
    unicode = models.CharField(max_length=300, null=True)
    symptoms_started = models.DateField(null=True, blank=True)
    how_often = models.TextField(null=True, blank=True)
    how_long = models.TextField(null=True, blank=True)
    describe = models.TextField(null=True, blank=True)
    severity = models.CharField(
        max_length=50, choices=SEVERITY, null=True, blank=True)
    affects_walking = models.BooleanField()
    affects_bathing = models.BooleanField()
    affects_dressing = models.BooleanField()
    affects_eating = models.BooleanField()
    affects_hygiene = models.BooleanField()
    affects_sleeping = models.BooleanField()
    affects_toilet = models.BooleanField()
    affects_sex = models.BooleanField()
    affects_bowel = models.BooleanField()
    affects_urination = models.BooleanField()
    affects_activities = models.TextField(null=True, blank=True)
    activities_worse = models.TextField(null=True, blank=True)
    activities_improves = models.TextField(null=True, blank=True)
    other_symptoms = models.TextField(null=True, blank=True)
    medications = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)


class ChildhoodIllness(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    unicode = models.CharField(max_length=300, null=True)
    measles = models.BooleanField()
    mumps = models.BooleanField()
    rubella = models.BooleanField()
    asthma = models.BooleanField()
    primary_complex = models.BooleanField()
    chicken_pox = models.BooleanField()
    others = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)


class AdultIllness(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    unicode = models.CharField(max_length=300, null=True)
    diabetes = models.BooleanField()
    hypertension = models.BooleanField()
    stroke = models.BooleanField()
    arthritis = models.BooleanField()
    tuberculosis = models.BooleanField()
    heart_disease = models.BooleanField()
    thyroid = models.BooleanField()
    asthma = models.BooleanField()
    others = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return 'unicode: ' + str(self.unicode)


class HistoryOfImmunization(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    unicode = models.CharField(max_length=300, null=True)
    surgeries = models.TextField(null=True, blank=True)
    medical_allergies = models.TextField(null=True, blank=True)
    other_allergies = models.TextField(null=True, blank=True)
    hepatitis_a = models.BooleanField()
    hepatitis_b = models.BooleanField()
    polio = models.BooleanField()
    measles = models.BooleanField()
    influenza = models.BooleanField()
    varicella = models.BooleanField()
    influenza_b = models.BooleanField()
    pneumococcal = models.BooleanField()
    meningococcal = models.BooleanField()
    hpv = models.BooleanField()
    others_immunization = models.TextField(null=True, blank=True)
    tuberculosis_test = models.BooleanField()
    stool_test = models.BooleanField()
    colonoscopy = models.BooleanField()
    blood_test = models.BooleanField()
    x_ray = models.BooleanField()
    ct_scan_ultrasound = models.BooleanField()
    pap_smears = models.BooleanField()
    mammograms = models.BooleanField()
    others_test = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return 'unicode: ' + str(self.unicode)


class FamilyHistory(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    unicode = models.CharField(max_length=300, null=True)
    diabetes = models.BooleanField()
    hypertension = models.BooleanField()
    stroke = models.BooleanField()
    arthritis = models.BooleanField()
    tuberculosis = models.BooleanField()
    heart_disease = models.BooleanField()
    thyroid = models.BooleanField()
    asthma = models.BooleanField()
    others = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return 'unicode: ' + str(self.unicode)


class PersonalAndSocialHistory(models.Model):
    HOW_OFTEN_DRINKING = (
        ('everyday', 'Everyday'),
        ('most days of the week', 'Most days of the week'),
        ('1-2x per week', '1-2x per week'),
        ('every month', 'Every month'),
        ('occasional', 'Occasional')
    )

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    unicode = models.CharField(max_length=300, null=True)
    physical_activity = models.TextField(null=True, blank=True)
    healthy_foods = models.TextField(null=True, blank=True)
    course_year_level = models.CharField(max_length=255, null=True, blank=True)
    occupation = models.CharField(max_length=255, null=True, blank=True)
    sticks_per_day = models.CharField(max_length=255, null=True, blank=True)
    years_smoking = models.CharField(max_length=255, null=True, blank=True)
    when_stop_smoking = models.CharField(max_length=255, null=True, blank=True)
    bottles_per_day = models.CharField(max_length=255, null=True, blank=True)
    how_often_drinking = models.CharField(
        max_length=255, null=True, blank=True)
    substance_drugs = models.TextField(null=True, blank=True)
    when_drugs_used = models.CharField(max_length=255, null=True, blank=True)
    how_often_drugs = models.CharField(
        max_length=255, null=True, blank=True, choices=HOW_OFTEN_DRINKING)
    last_time_drugs = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return 'unicode: ' + str(self.unicode)


class FunctionalHistory(models.Model):
    ASSISTIVE_DEVICE = (
        ('no', 'No.'),
        ('cane', 'Yes. I use a cane.'),
        ('walker', 'Yes. I use a walker.'),
        ('wheelchair', 'Yes. I use a wheelchair')
    )
    DRIVE = (
        ('no', 'No.'),
        ('yes', 'Yes.')
    )
    SUPPORT = (
        ('100%', '100%'),
        ('75%', '75%'),
        ('50%', '50%'),
        ('25%', '25%')
    )
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    unicode = models.CharField(max_length=300, null=True)
    assistive_walking = models.CharField(
        max_length=50, null=True, blank=True, choices=ASSISTIVE_DEVICE)
    drive_own = models.CharField(
        max_length=5, null=True, blank=True, choices=DRIVE)
    affects_walking = models.BooleanField()
    affects_bathing = models.BooleanField()
    affects_dressing = models.BooleanField()
    affects_eating = models.BooleanField()
    affects_hygiene = models.BooleanField()
    affects_sleeping = models.BooleanField()
    affects_toilet = models.BooleanField()
    affects_sex = models.BooleanField()
    affects_bowel = models.BooleanField()
    affects_urination = models.BooleanField()
    needs_support = models.CharField(
        max_length=5, null=True, blank=True, choices=SUPPORT)
    assistive_devices = models.TextField(null=True, blank=True)
    difficulties_activities = models.TextField(null=True, blank=True)
    difficulties_assistance = models.TextField(null=True, blank=True)
    difficulties_in_complicated = models.TextField(null=True, blank=True)
    difficulties_in_verbal = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return 'unicode: ' + str(self.unicode)


class GeneralSystem(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    unicode = models.CharField(max_length=300, null=True)
    fever = models.BooleanField()
    fatigue = models.BooleanField()
    weight_change = models.BooleanField()
    weakness = models.BooleanField()
    none = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return 'unicode: ' + str(self.unicode)


class SkinProblem(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    unicode = models.CharField(max_length=300, null=True)
    rashes = models.BooleanField()
    lumps = models.BooleanField()
    sores = models.BooleanField()
    itching = models.BooleanField()
    dryness = models.BooleanField()
    changes_in_color = models.BooleanField()
    changes_in_hair_nails = models.BooleanField()
    none = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return 'unicode: ' + str(self.unicode)


class Heent(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    unicode = models.CharField(max_length=300, null=True)
    headache = models.BooleanField()
    dizziness = models.BooleanField()
    lightheadedness = models.BooleanField()
    changes_in_vision = models.BooleanField()
    eye_pain = models.BooleanField()
    eye_redness = models.BooleanField()
    double_vision = models.BooleanField()
    watery_eyes = models.BooleanField()
    poor_hearing = models.BooleanField()
    ringing_ears = models.BooleanField()
    ear_discharge = models.BooleanField()
    stuffy_nose = models.BooleanField()
    nasal_discharge = models.BooleanField()
    nasal_bleeding = models.BooleanField()
    unusual_odors = models.BooleanField()
    mouth_sores = models.BooleanField()
    altered_taste = models.BooleanField()
    sore_tongue = models.BooleanField()
    gum_problem = models.BooleanField()
    sore_throat = models.BooleanField()
    hoarseness = models.BooleanField()
    swelling = models.BooleanField()
    diffuculty_swallowing = models.BooleanField()
    none = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return 'unicode: ' + str(self.unicode)


class Breast(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    unicode = models.CharField(max_length=300, null=True)
    breast_lumps = models.BooleanField()
    nipple_discharge = models.BooleanField()
    bleeding = models.BooleanField()
    breast_swelling = models.BooleanField()
    breast_tenderness = models.BooleanField()
    none = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return 'unicode: ' + str(self.unicode)


class Pulmonary(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    unicode = models.CharField(max_length=300, null=True)
    cough = models.BooleanField()
    sputum = models.BooleanField()
    bloody_sputum = models.BooleanField()
    chest_pain = models.BooleanField()
    shortness_breath = models.BooleanField()
    none = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return 'unicode: ' + str(self.unicode)


class Cardiovascular(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    unicode = models.CharField(max_length=300, null=True)
    chest_pain = models.BooleanField()
    shortness_of_breath = models.BooleanField()
    palpitations = models.BooleanField()
    cough = models.BooleanField()
    swelling_of_ankles = models.BooleanField()
    trouble_lying = models.BooleanField()
    fatigue = models.BooleanField()
    none = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return 'unicode: ' + str(self.unicode)


class Gastrointestinal(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    unicode = models.CharField(max_length=300, null=True)
    changes_in_appetite = models.BooleanField()
    nausea = models.BooleanField()
    vomitting = models.BooleanField()
    diarrhea = models.BooleanField()
    constipation = models.BooleanField()
    changes_in_bowel = models.BooleanField()
    bleeding_rectum = models.BooleanField()
    hemorrhoids = models.BooleanField()
    decreased_stool = models.BooleanField()
    none = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return 'unicode: ' + str(self.unicode)


class Genitourinary(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    unicode = models.CharField(max_length=300, null=True)
    painful_urination = models.BooleanField()
    increased_decreased_frequency = models.BooleanField()
    bloody_urine = models.BooleanField()
    trouble_urination = models.BooleanField()
    none = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return 'unicode: ' + str(self.unicode)


class Gynecologic(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    unicode = models.CharField(max_length=300, null=True)
    pregnancies = models.CharField(max_length=255, null=True, blank=True)
    miscarriages = models.CharField(max_length=255, null=True, blank=True)
    last_period = models.TextField(null=True, blank=True)
    irregular_menstration = models.BooleanField()
    vaginal_bleeding = models.BooleanField()
    vaginal_discharge = models.BooleanField()
    cessation_of_periods = models.BooleanField()
    hot_flashes = models.BooleanField()
    vaginal_itching = models.BooleanField()
    sexual_dysfunction = models.BooleanField()
    none = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return 'unicode: ' + str(self.unicode)


class Endocrine(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    unicode = models.CharField(max_length=300, null=True)
    hot_or_cold = models.BooleanField()
    fatigue = models.BooleanField()
    changes_hair_skin = models.BooleanField()
    shaking = models.BooleanField()
    none = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return 'unicode: ' + str(self.unicode)


class Musculoskeletal(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    unicode = models.CharField(max_length=300, null=True)
    joints_muscle_pain = models.BooleanField()
    stiffness = models.BooleanField()
    motion_limitation = models.BooleanField()
    muscle_atrophy = models.BooleanField()
    muscle_hypertrophy = models.BooleanField()
    none = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return 'unicode: ' + str(self.unicode)


class Neurologic(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    unicode = models.CharField(max_length=300, null=True)
    numbness = models.BooleanField()
    weakness = models.BooleanField()
    needle_sensation = models.BooleanField()
    changes_in_mood = models.BooleanField()
    changes_in_memory = models.BooleanField()
    tremors = models.BooleanField()
    seizures = models.BooleanField()
    none = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return 'unicode: ' + str(self.unicode)
