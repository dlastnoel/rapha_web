from django.urls import path
from . import views

urlpatterns = [
    path('', views.overview, name='api-overview'),

    path('save-contact/', views.saveContact, name='save-contact'),
    path('update-client/', views.updateClient, name='update-client'),
    path('get-client/', views.getClient, name='get-client'),
    path('add-patient/', views.addPatient, name='add-patient'),
    path('get-patients/', views.getPatients, name='get-patients'),
    path('get-patient/', views.getPatient, name='get-patient'),
    path('add-chief-complaint/', views.addChiefComplaint,
         name='add-chief-complaint'),
    path('add-present-illness-image/', views.addPresentIllnessImage,
         name='add-present-illness-image'),
    path('add-present-illness/', views.addPresentIllness,
         name='add-present-illness'),
    path('add-childhood-illness/', views.addChildhoodIllness,
         name='add-childhood-illness/'),
    path('add-adult-illness/', views.addAdultIllness,
         name='add-adult-illness'),
    path('add-history-of-immunization/', views.addHistoryOfImmunization,
         name='add-history-of-immunization'),
    path('add-family-history/', views.addFamilyHistory,
         name='add-family-history'),
    path('add-personal-and-social-history/', views.addPersonalAndSocialHistory,
         name='add-personal-and-social-history'),
    path('add-functional-history/', views.addFunctionalHistory,
         name='add-functional-history'),
    path('add-general-system/', views.addGeneralSystem,
         name='add-general-system'),
    path('add-skin-problem/', views.addSkinProblem,
         name='add-skin-problem'),
    path('add-heent/', views.addHeent,
         name='add-heent'),
    path('add-breast/', views.addBreast,
         name='add-breast'),
    path('add-pulmonary/', views.addPulmonary,
         name='add-pulmonary'),
    path('add-cardiovascular/', views.addCardiovascular,
         name='add-cardiovascular'),
    path('add-gastronintestinal/', views.addGastrointestinal,
         name='add-gastronintestinal'),
    path('add-genitourinary/', views.addGenitourinary,
         name='add-genitourinary'),
    path('add-gynecologic/', views.addGynecologic,
         name='add-gastronintestinal'),
    path('add-endocrine/', views.addEndocrine,
         name='add-endocrine'),
    path('add-musculoskeletal/', views.addMusculosketal,
         name='add-musculoskeletal'),
    path('add-neurologic/', views.addNeurologic,
         name='add-neurologic'),
    # path('add-patient-checkup/', views.addPatientCheckup,
    #      name='add-patient-checkup'),
    path('get-doctors/', views.getDoctors, name='get-doctors'),
    path('get-doctor/', views.getDoctor, name='get-doctor'),
    path('get-schedule/', views.getSchedule, name='get-schedule'),
    path('get-slot/', views.getSlot, name='get-slot'),
    path('get-appointments/', views.getDoctorAppointments, name='get-appointments'),
    path('create-appointment/', views.createAppointment,
         name='create-appointment'),
    # path('set-limit/', views.setScheduleLimit, name='set-limit'),

]
