from django.urls import path
from . import views
# from doctors import views as doctor_views

urlpatterns = [
    path('', views.overview, name='api-overview'),

    path('save-contact/', views.saveContact, name='save-contact'),
    path('update-client/', views.updateClient, name='update-client'),
    path('get-client/', views.getClient, name='get-client'),
    path('get-clients/', views.getClients, name='get-clients'),
    path('add-patient/', views.addPatient, name='add-patient'),
    path('get-patients/', views.getPatients, name='get-patients'),
    path('get-patient/', views.getPatient, name='get-patient'),
    # path('pdf_download/', doctor_views.ViewPDF.as_view(), name="pdf_download"),

    # Medical endpoints
    # Add
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
    path('add-patient-data/', views.addPatientData,
         name='add-patient-data'),
    path('cancel-patient-data/', views.cancelPatientData,
         name='cancel-patient-data'),

    # Medical endpoints
    # Get
    path('get-chief-complaint/', views.getChiefComplaint,
         name='get-chief-complaint'),
    path('get-present-illness-image/', views.getPresentIllnessImage,
         name='get-present-illness-image'),
    path('get-present-illness/', views.getPresentIllness,
         name='get-present-illness'),
    path('get-childhood-illness/', views.getChildhoodIllness,
         name='get-childhood-illness/'),
    path('get-adult-illness/', views.getAdultIllness,
         name='get-adult-illness'),
    path('get-history-of-immunization/', views.getHistoryOfImmunization,
         name='get-history-of-immunization'),
    path('get-family-history/', views.getFamilyHistory,
         name='get-family-history'),
    path('get-personal-and-social-history/', views.getPersonalAndSocialHistory,
         name='get-personal-and-social-history'),
    path('get-functional-history/', views.getFunctionalHistory,
         name='get-functional-history'),
    path('get-general-system/', views.getGeneralSystem,
         name='get-general-system'),
    path('get-skin-problem/', views.getSkinProblem,
         name='get-skin-problem'),
    path('get-heent/', views.getHeent,
         name='get-heent'),
    path('get-breast/', views.getBreast,
         name='get-breast'),
    path('get-pulmonary/', views.getPulmonary,
         name='get-pulmonary'),
    path('get-cardiovascular/', views.getCardiovascular,
         name='get-cardiovascular'),
    path('get-gastronintestinal/', views.getGastrointestinal,
         name='get-gastronintestinal'),
    path('get-genitourinary/', views.getGenitourinary,
         name='get-genitourinary'),
    path('get-gynecologic/', views.getGynecologic,
         name='get-gastronintestinal'),
    path('get-endocrine/', views.getEndocrine,
         name='get-endocrine'),
    path('get-musculoskeletal/', views.getMusculosketal,
         name='get-musculoskeletal'),
    path('get-neurologic/', views.getNeurologic,
         name='get-neurologic'),
    path('get-patient-data/', views.getPatientData,
         name='get-patient-data'),


    # path('add-patient-checkup/', views.addPatientCheckup,
    #      name='add-patient-checkup'),
    path('get-doctors/', views.getDoctors, name='get-doctors'),
    path('get-doctor/', views.getDoctor, name='get-doctor'),
    path('get-schedule/', views.getSchedule, name='get-schedule'),
    path('get-slot/', views.getSlot, name='get-slot'),
    path('get-appointments/', views.getDoctorAppointments, name='get-appointments'),
    path('create-appointment/', views.createAppointment,
         name='create-appointment'),
    path('delete-medical-data/', views.deleteMedicalData,
         name='delete-medical-data'),
    # path('set-limit/', views.setScheduleLimit, name='set-limit'),

]
