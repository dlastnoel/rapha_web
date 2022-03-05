from ast import Mult
from operator import ge, ne
import jwt
import json
from rest_framework.response import Response
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser, FileUploadParser
from rest_framework import viewsets
from . serializers import *
from clients.models import Client
from patients.models import Patient, PresentIllnessImage
from patients.forms import PresentIllnessImageForm
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
def addPatient(request):
    token = jwt.decode(request.data['client'],
                       request.data['code'], algorithms="HS256")
    request.data['client'] = token['id']

    patient = PatientSerializer(data=request.data)

    if patient.is_valid():
        patient.save()

    return Response(patient.data)


@api_view(['POST'])
def getPatients(request):
    token = jwt.decode(request.data['client'],
                       request.data['code'], algorithms="HS256")
    client_id = token['id']
    if Patient.objects.filter(client=client_id).exists():
        patients = Patient.objects.filter(client=client_id)
        serializer = PatientSerializer(patients,  many=True)
        return Response(serializer.data)


@api_view(['POST'])
def getPatient(request):
    patient = Patient.objects.get(id=request.data['id'])
    serializer = PatientSerializer(patient, many=False)
    return Response(serializer.data)


@api_view(['POST'])
def addChiefComplaint(request):
    chief_complaint = ChiefComplaintSerializer(data=request.data)
    if chief_complaint.is_valid():
        chief_complaint.save()
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
    return Response(present_illness.data)


@api_view(['POST'])
def addChildhoodIllness(request):
    childhood_illness = ChildhoodSerializer(data=request.data)
    if childhood_illness.is_valid():
        childhood_illness.save()
    return Response(childhood_illness.data)


@api_view(['POST'])
def addAdultIllness(request):
    adult_illness = AdultIllnessSerialzer(data=request.data)
    if adult_illness.is_valid():
        adult_illness.save()
    return Response(adult_illness.data)


@api_view(['POST'])
def addHistoryOfImmunizationHistory(request):
    history_of_immunization = HistoryOfImmunizationSerialzer(data=request.data)
    if history_of_immunization.is_valid():
        history_of_immunization.save()
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
    return Response(personal_and_social_history.data)


@api_view(['POST'])
def addFunctionalHistory(request):
    functional_history = FunctionalHistorySerializer(data=request.data)
    if functional_history.is_valid():
        functional_history.save()
    return Response(functional_history.data)


@api_view(['POST'])
def addGeneralSystem(request):
    general_system = GeneralSystemSerializer(data=request.data)
    if general_system.is_valid():
        general_system.save()
    return Response(general_system.data)


@api_view(['POST'])
def addSkinProblem(request):
    skin_problem = SkinProblemSerializer(data=request.data)
    if skin_problem.is_valid():
        skin_problem.save()
    return Response(skin_problem.data)


@api_view(['POST'])
def addHeent(request):
    heent = HeentSerializer(data=request.data)
    if heent.is_valid():
        heent.save()
    return Response(heent.data)


@api_view(['POST'])
def addBreast(request):
    breast = BreastSerializer(data=request.data)
    if breast.is_valid():
        breast.save()
    return Response(breast.data)


@api_view(['POST'])
def addPulmonary(request):
    pulmonary = PulmonarySerializer(data=request.data)
    if pulmonary.is_valid():
        pulmonary.save()
    return Response(pulmonary.data)


@api_view(['POST'])
def addCardiovascular(request):
    cardiovascular = CardiovascularSerializer(data=request.data)
    if cardiovascular.is_valid():
        cardiovascular.save()
    return Response(cardiovascular.data)


@api_view(['POST'])
def addGastrointestinal(request):
    gastroinstestinal = GastrointestinalSerializer(data=request.data)
    if gastroinstestinal.is_valid():
        gastroinstestinal.save()
    return Response(gastroinstestinal.data)


@api_view(['POST'])
def addGenitourinary(request):
    genitourinary = GenitourinarySerializer(data=request.data)
    if genitourinary.is_valid():
        genitourinary.save()
    return Response(genitourinary.data)


@api_view(['POST'])
def addGynecologic(request):
    gynecologic = GynecologicSerializer(data=request.data)
    if gynecologic.is_valid():
        gynecologic.save()
    return Response(gynecologic.data)


@api_view(['POST'])
def addEndocrine(request):
    endocrine = EndocrineSerializer(data=request.data)
    if endocrine.is_valid():
        endocrine.save()
    return Response(endocrine.data)


@api_view(['POST'])
def addMusculosketal(request):
    musculosketal = MusculoskeletalSerializer(data=request.data)
    if musculosketal.is_valid():
        musculosketal.save()
    return Response(musculosketal.data)


@api_view(['POST'])
def addNeurologic(request):
    neurologic = NeurologicSerializer(data=request.data)
    if neurologic.is_valid():
        neurologic.save()
    return Response(neurologic.data)
