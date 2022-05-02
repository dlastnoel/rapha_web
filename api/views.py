from ast import Mult
from operator import ge, ne
import jwt
import json
from datetime import date, timedelta
from rest_framework.response import Response
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser, FileUploadParser
from rest_framework import viewsets

from appointments.views import appointment
from . serializers import *
from clients.models import Client
from patients.models import Patient, PresentIllnessImage
from patients.forms import PresentIllnessImageForm
from appointments.models import Appoinment
from rest_framework import status


@api_view(['GET'])
def overview(request):
    routes = [
        {'GET': 'api/save-contact/'},
        {'POST': 'api/update-client/'},
        {'POST': 'api/get-client/'},
        {'POST': 'api/add-patient/'},
        {'POST': 'api/get-patients/'},
        {'POST': 'api/add-chief-complaint/'},
        {'POST': 'api/present-illness-image/'},
        {'POST': 'api/add-present-illness/'},
        {'POST': 'api/add-childhood-illness/'},
        {'POST': 'api/add-history-of-immunization-history/'},
        {'POST': 'api/add-family-history/'},
        {'POST': 'api/add-personal-and-social-history/'},
        {'POST': 'api/add-general-system/'},
        {'POST': 'api/add-skin-problem/'},
        {'POST': 'api/add-breast/'},
        {'POST': 'api/add-pulmonary/'},
        {'POST': 'api/add-cardiovascular/'},
        {'POST': 'api/add-gastronintestinal/'},
        {'POST': 'api/add-genitourinary/'},
        {'POST': 'api/add-gynecologic/'},
        {'POST': 'api/add-endocrine/'},
        {'POST': 'api/add-musculoskeletal/'},
        {'POST': 'api/add-neurologic/'},

    ]
    return Response(routes)


@api_view(['GET'])
def saveContact(request):
    serializer = ContactTokenSerializer(data=request.query_params)
    print(serializer)
    if serializer.is_valid():
        serializer.save()
        client = Client.objects.latest('created_at')
        client_serializer = ClientIdSerializer(client, many=False)
    return Response(client_serializer.data)


@api_view(['POST'])
def updateClient(request):
    client = Client.objects.latest('created_at')
    serializer = ClientSerializer(instance=client, data=request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(['POST'])
def getClient(request):
    client = Client.objects.get(
        username=request.data['username'], contact=request.data['contact'])
    serializer = ClientSerializer(client)

    return Response(serializer.data)


@api_view(['POST'])
def getClientByPatientId(request):
    client = Client.objects.get(patient=request.data['patient'])
    serializer = ClientSerializer(client)

    return Response(serializer.data)


@api_view(['GET'])
def getClients(request):
    client = Client.objects.all()
    serializer = ClientSerializer(client, many=True)

    return Response(serializer.data)


@api_view(['POST'])
def addPatient(request):
    token = jwt.decode(request.data['client'],
                       request.data['code'], algorithms="HS256")

    mutable = request.data._mutable
    request.data._mutable = True
    request.data['client'] = token['id']
    request.data._mutable = mutable
    patient = PatientSerializer(data=request.data)

    if patient.is_valid():
        patient.save()
    else:
        print(patient.errors)
    last_patient = Patient.objects.latest('created_at')
    serializer = PatientSerializer(last_patient, many=False)
    return Response(serializer.data)


@api_view(['POST'])
def getPatients(request):
    token = jwt.decode(request.data['client'],
                       request.data['code'], algorithms="HS256")
    client_id = token['id']
    if Patient.objects.filter(client=client_id).exists():
        patients = Patient.objects.filter(client=client_id)
        serializer = PatientSerializer(patients,  many=True)
        return Response(serializer.data)


@api_view(['GET'])
def getRawPatients(request):
    patients = Patient.objects.all()
    serializer = PatientSerializer(patients,  many=True)
    return Response(serializer.data)


@api_view(['POST'])
def getPatient(request):
    patient = Patient.objects.get(id=request.data['id'])
    serializer = PatientSerializer(patient, many=False)
    return Response(serializer.data)

# --------------------
# --------------------
# MEDICAL API ENDPOINTS
# --------------------
# --------------------


# --------------------
# --------------------
# ADD CALLERS
# --------------------
# --------------------
@api_view(['POST'])
def addChiefComplaint(request):
    chief_complaint = ChiefComplaintSerializer(data=request.data)
    if chief_complaint.is_valid():
        chief_complaint.save()
    else:
        print(chief_complaint.errors)
    return Response(chief_complaint.data)


@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser, FileUploadParser])
def addPresentIllnessImage(request):
    form = PresentIllnessImageForm(request.data, request.FILES)
    if form.is_valid():
        form.save()
    return Response({'details': 'Image uploaded successfully'})


@api_view(['POST'])
def addPresentIllness(request):
    present_illness = PresentIllnessSerializer(data=request.data)
    if present_illness.is_valid():
        present_illness.save()
    else:
        print(present_illness.errors)
    return Response(present_illness.data)


@api_view(['POST'])
def addChildhoodIllness(request):
    childhood_illness = ChildhoodSerializer(data=request.data)
    if childhood_illness.is_valid():
        childhood_illness.save()
    else:
        print(childhood_illness.errors)
    return Response(childhood_illness.data)


@api_view(['POST'])
def addAdultIllness(request):
    adult_illness = AdultIllnessSerialzer(data=request.data)
    if adult_illness.is_valid():
        adult_illness.save()
    else:
        print(adult_illness.errors)
    return Response(adult_illness.data)


@api_view(['POST'])
def addHistoryOfImmunization(request):
    history_of_immunization = HistoryOfImmunizationSerialzer(data=request.data)
    if history_of_immunization.is_valid():
        history_of_immunization.save()
    else:
        print(history_of_immunization.errors)
    return Response(history_of_immunization.data)


@api_view(['POST'])
def addFamilyHistory(request):
    family_history = FamilyHistorySerializer(data=request.data)
    if family_history.is_valid():
        family_history.save()
    return Response(family_history.data)


@api_view(['POST'])
def addPersonalAndSocialHistory(request):
    personal_and_social_history = PersonalAndSocialHistorySerializer(
        data=request.data)
    if personal_and_social_history.is_valid():
        personal_and_social_history.save()
    else:
        print(personal_and_social_history.errors)
    return Response(personal_and_social_history.data)


@api_view(['POST'])
def addFunctionalHistory(request):
    functional_history = FunctionalHistorySerializer(data=request.data)
    if functional_history.is_valid():
        functional_history.save()
    else:
        print(functional_history.errors)
    return Response(functional_history.data)


@api_view(['POST'])
def addGeneralSystem(request):
    general_system = GeneralSystemSerializer(data=request.data)
    if general_system.is_valid():
        general_system.save()
    else:
        print(general_system.errors)
    return Response(general_system.data)


@api_view(['POST'])
def addSkinProblem(request):
    skin_problem = SkinProblemSerializer(data=request.data)
    if skin_problem.is_valid():
        skin_problem.save()
    else:
        print(skin_problem.errors)
    return Response(skin_problem.data)


@api_view(['POST'])
def addHeent(request):
    heent = HeentSerializer(data=request.data)
    if heent.is_valid():
        heent.save()
    else:
        print(heent.errors)
    return Response(heent.data)


@api_view(['POST'])
def addBreast(request):
    breast = BreastSerializer(data=request.data)
    if breast.is_valid():
        breast.save()
    else:
        print(breast.errors)
    return Response(breast.data)


@api_view(['POST'])
def addPulmonary(request):
    pulmonary = PulmonarySerializer(data=request.data)
    if pulmonary.is_valid():
        pulmonary.save()
    else:
        print(pulmonary.errors)
    return Response(pulmonary.data)


@api_view(['POST'])
def addCardiovascular(request):
    cardiovascular = CardiovascularSerializer(data=request.data)
    if cardiovascular.is_valid():
        cardiovascular.save()
    else:
        print(cardiovascular.errors)
    return Response(cardiovascular.data)


@api_view(['POST'])
def addGastrointestinal(request):
    gastroinstestinal = GastrointestinalSerializer(data=request.data)
    if gastroinstestinal.is_valid():
        gastroinstestinal.save()
    else:
        print(gastroinstestinal.errors)
    return Response(gastroinstestinal.data)


@api_view(['POST'])
def addGenitourinary(request):
    genitourinary = GenitourinarySerializer(data=request.data)
    if genitourinary.is_valid():
        genitourinary.save()
    else:
        print(genitourinary.errors)
    return Response(genitourinary.data)


@api_view(['POST'])
def addGynecologic(request):
    gynecologic = GynecologicSerializer(data=request.data)
    if gynecologic.is_valid():
        gynecologic.save()
    else:
        print(gynecologic.errors)
    return Response(gynecologic.data)


@api_view(['POST'])
def addEndocrine(request):
    endocrine = EndocrineSerializer(data=request.data)
    if endocrine.is_valid():
        endocrine.save()
    else:
        print(endocrine.errors)
    return Response(endocrine.data)


@api_view(['POST'])
def addMusculosketal(request):
    musculosketal = MusculoskeletalSerializer(data=request.data)
    if musculosketal.is_valid():
        musculosketal.save()
    else:
        print(musculosketal.errors)
    return Response(musculosketal.data)


@api_view(['POST'])
def addNeurologic(request):
    neurologic = NeurologicSerializer(data=request.data)
    if neurologic.is_valid():
        neurologic.save()
    else:
        print(neurologic.errors)
    return Response(neurologic.data)


@api_view(['POST'])
def addPatientData(request):
    patient = Appoinment.objects.get(
        id=request.data['id'])
    serializer = AppointmentSerializer(instance=patient, data=request.data)
    if serializer.is_valid():
        serializer.save()
    else:
        print(serializer.errors)

    return Response(serializer.data)


@api_view(['POST'])
def cancelPatientData(request):
    patient = Appoinment.objects.get(
        id=request.data['id'])

    patient.doctor = None
    patient.checkup_date = None
    patient.checkup_start = None
    patient.checkup_end = None
    patient.save()

    serializer = AppointmentSerializer(patient, many=False)
    return Response(serializer.data)


# --------------------
# --------------------
# GET CALLERS
# --------------------
# --------------------

@ api_view(['POST'])
def getChiefComplaint(request):
    chief_complaint = ChiefComplaint.objects.get(
        unicode=request.data['unicode'])
    serializer = ChiefComplaintSerializer(chief_complaint, many=False)

    return Response(serializer.data)


@ api_view(['POST'])
def getPresentIllnessImage(request):
    present_illness_image = PresentIllnessImage.objects.get(
        unicode=request.data['unicode'])
    serializer = PresentIllnessImageSerializer(
        present_illness_image, many=False)

    return Response(serializer.data)


@ api_view(['POST'])
def getPresentIllness(request):
    presennt_illness = PresentIllness.objects.get(
        unicode=request.data['unicode'])
    serializer = PresentIllnessSerializer(presennt_illness, many=False)

    return Response(serializer.data)


@ api_view(['POST'])
def getChildhoodIllness(request):
    childhood_image = ChildhoodIllness.objects.get(
        unicode=request.data['unicode'])
    serializer = ChildhoodSerializer(childhood_image, many=False)

    return Response(serializer.data)


@ api_view(['POST'])
def getAdultIllness(request):
    adult_illness = AdultIllness.objects.get(unicode=request.data['unicode'])
    serializer = AdultIllnessSerialzer(adult_illness, many=False)

    return Response(serializer.data)


@ api_view(['POST'])
def getHistoryOfImmunization(request):
    history_of_immunization = HistoryOfImmunization.objects.get(
        unicode=request.data['unicode'])
    serializer = HistoryOfImmunizationSerialzer(
        history_of_immunization, many=False)

    return Response(serializer.data)


@ api_view(['POST'])
def getFamilyHistory(request):
    family_history = FamilyHistory.objects.get(unicode=request.data['unicode'])
    serializer = FamilyHistorySerializer(family_history, many=False)

    return Response(serializer.data)


@ api_view(['POST'])
def getPersonalAndSocialHistory(request):
    print(request.data['unicode'])
    personal_and_social_history = PersonalAndSocialHistory.objects.get(
        unicode=request.data['unicode'])
    serializer = PersonalAndSocialHistorySerializer(
        personal_and_social_history, many=False)

    return Response(serializer.data)


@ api_view(['POST'])
def getFunctionalHistory(request):
    functional_history = FunctionalHistory.objects.get(
        unicode=request.data['unicode'])
    serializer = FunctionalHistorySerializer(functional_history, many=False)

    return Response(serializer.data)


@ api_view(['POST'])
def getGeneralSystem(request):
    general_system = GeneralSystem.objects.get(unicode=request.data['unicode'])
    serializer = GeneralSystemSerializer(general_system, many=False)

    return Response(serializer.data)


@ api_view(['POST'])
def getSkinProblem(request):
    skin_problem = SkinProblem.objects.get(unicode=request.data['unicode'])
    serializer = SkinProblemSerializer(skin_problem, many=False)

    return Response(serializer.data)


@ api_view(['POST'])
def getHeent(request):
    heent = Heent.objects.get(unicode=request.data['unicode'])
    serializer = HeentSerializer(heent, many=False)

    return Response(serializer.data)


@ api_view(['POST'])
def getBreast(request):
    breast = Breast.objects.get(unicode=request.data['unicode'])
    serializer = BreastSerializer(breast, many=False)

    return Response(serializer.data)


@ api_view(['POST'])
def getPulmonary(request):
    pulmonary = Pulmonary.objects.get(unicode=request.data['unicode'])
    serializer = PulmonarySerializer(pulmonary, many=False)

    return Response(serializer.data)


@ api_view(['POST'])
def getCardiovascular(request):
    cardiovascular = Cardiovascular.objects.get(
        unicode=request.data['unicode'])
    serializer = CardiovascularSerializer(cardiovascular, many=False)

    return Response(serializer.data)


@ api_view(['POST'])
def getGastrointestinal(request):
    gastrointestinal = Gastrointestinal.objects.get(
        unicode=request.data['unicode'])
    serializer = GastrointestinalSerializer(gastrointestinal, many=False)

    return Response(serializer.data)


@ api_view(['POST'])
def getGenitourinary(request):
    genitourinary = Genitourinary.objects.get(unicode=request.data['unicode'])
    serializer = GenitourinarySerializer(genitourinary, many=False)

    return Response(serializer.data)


@ api_view(['POST'])
def getGynecologic(request):
    gynecologic = Gynecologic.objects.get(unicode=request.data['unicode'])
    serializer = GynecologicSerializer(gynecologic, many=False)

    return Response(serializer.data)


@ api_view(['POST'])
def getEndocrine(request):
    endocrine = Endocrine.objects.get(unicode=request.data['unicode'])
    serializer = EndocrineSerializer(endocrine, many=False)

    return Response(serializer.data)


@ api_view(['POST'])
def getMusculosketal(request):
    musculoskeletal = Musculoskeletal.objects.get(
        unicode=request.data['unicode'])
    serializer = MusculoskeletalSerializer(musculoskeletal, many=False)

    return Response(serializer.data)


@ api_view(['POST'])
def getNeurologic(request):
    neurologic = Neurologic.objects.get(unicode=request.data['unicode'])
    serializer = NeurologicSerializer(neurologic, many=False)

    return Response(serializer.data)


@ api_view(['POST'])
def getPatientData(request):
    if request.data['status'] == 'for_appointment':
        patient_data = Appoinment.objects.filter(
            patient=request.data['patient']).filter(doctor__isnull=True).order_by('-created_at')
        serializer = AppointmentSerializer(patient_data, many=True)
        return Response(serializer.data)

    if request.data['status'] == 'has_appointment':
        patient_data = Appoinment.objects.filter(
            patient=request.data['patient']).filter(doctor__isnull=False).filter(status='none').order_by('-created_at')
        serializer = AppointmentSerializer(patient_data, many=True)
        return Response(serializer.data)

    else:
        patient_data = Appoinment.objects.filter(
            patient=request.data['patient']).filter(status='done').order_by('-created_at')
        serializer = AppointmentSerializer(patient_data, many=True)
        return Response(serializer.data)

## _____________ END ______________ ##


@ api_view(['GET'])
def getDoctors(request):
    doctors = Doctor.objects.order_by('specialization')
    serializer = DoctorSerializer(doctors, many=True)

    return Response(serializer.data)


@ api_view(['POST'])
def getDoctor(request):
    doctor = Doctor.objects.get(id=request.data['id'])
    serializer = DoctorSerializer(doctor, many=False)

    return Response(serializer.data)


# @api_view(['POST'])
# def addPatientCheckup(request):
#     patient_data = PatientCheckupSerializer(data=request.data)
#     if patient_data.is_valid():
#         patient_data.save()

#     return Response(patient_data.data)

@ api_view(['POST'])
def createAppointment(request):
    serializer = AppointmentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    else:
        print(serializer.errors)

    return Response(serializer.data)


@ api_view(['POST'])
def getDoctorAppointments(request):
    appointments = Appoinment.objects.filter(
        doctor=request.data['doctor']).filter(checkup_date=request.data['checkup_date'])
    serializer = AppointmentSerializer(appointments, many=True)
    if appointments.exists():
        return Response(serializer.data)
    return Response()


@ api_view(['GET'])
def getSlot(request):
    slot = Slot.objects.get(id=1)
    serializer = SlotSerializer(slot, many=False)

    return Response(serializer.data)


@ api_view(['POST'])
def getSchedule(request):
    schedule = Schedule.objects.filter(start__isnull=False).filter(
        end__isnull=False).filter(doctor=request.data['id'])
    # schedule = Schedule.objects.exclude(
    #     start__isnull=True).exclude(end__isnull=True).get(doctor=request.data['id'])
    serializer = ScheduleSerializer(schedule, many=True)

    return Response(serializer.data)


@ api_view(['POST'])
def deleteMedicalData(request):
    code = request.data['unicode']
    chief_complaint = ChiefComplaint.objects.get(
        unicode=code)
    present_illness_image = PresentIllnessImage.objects.get(
        unicode=code)
    present_illness = PresentIllness.objects.get(
        unicode=code)
    childhood_illness = ChildhoodIllness.objects.get(
        unicode=code)
    adult_illness = AdultIllness.objects.get(
        unicode=code)
    history_of_immunization = HistoryOfImmunization.objects.get(
        unicode=code)
    family_history = FamilyHistory.objects.get(
        unicode=code)
    personal_and_social_history = PersonalAndSocialHistory.objects.get(
        unicode=code)
    functional_history = FunctionalHistory.objects.get(
        unicode=code)
    generay_system = GeneralSystem.objects.get(
        unicode=code)
    skin_problem = SkinProblem.objects.get(unicode=code)
    heent = Heent.objects.get(unicode=code)
    breast = Breast.objects.get(unicode=code)
    pulmonary = Pulmonary.objects.get(unicode=code)
    cardiovascular = Cardiovascular.objects.get(
        unicode=code)
    gastrointestinal = Gastrointestinal.objects.get(
        unicode=code)
    genitourinary = Genitourinary.objects.get(
        unicode=code)
    gynecologic = Gynecologic.objects.get(
        unicode=code)
    endocrine = Endocrine.objects.get(unicode=code)
    musculoskeletal = Musculoskeletal.objects.get(
        unicode=code)
    neurologic = Neurologic.objects.get(unicode=code)
    appointment = Appoinment.objects.get(unicode=code)

    chief_complaint.delete()
    present_illness_image.delete()
    present_illness.delete()
    childhood_illness.delete()
    adult_illness.delete()
    history_of_immunization.delete()
    family_history.delete()
    personal_and_social_history.delete()
    functional_history.delete()
    generay_system.delete()
    skin_problem.delete()
    heent.delete()
    breast.delete()
    pulmonary.delete()
    cardiovascular.delete()
    gastrointestinal.delete()
    genitourinary.delete()
    gynecologic.delete()
    endocrine.delete()
    musculoskeletal.delete()
    neurologic.delete()
    appointment.delete()

    return Response('DELETE SUCCESSFUL')


# @api_view(['POST'])
# def setScheduleLimit(request):
#     # mutable = request.data._mutable
#     # request.data._mutable = True
#     request.data['limit'] = date.today() + timedelta(days=14)
#     # request.data._mutable = mutable
#     doctor = Doctor.objects.get(id=request.data['id'])
#     serializer = ScheduleLimiterSerializer(instance=doctor, data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#     else:
#         print(serializer.errors)

#     return Response(serializer.data)

# @api_view(['POST'])
# def getScheduleLimit(request):
#   doctor = Doctor.objects.get(id=request.data['id'])
#   serializer = DoctorSerializer(doctor, many=False)

#   return Response(serializer.data)
