from dataclasses import fields
from rest_framework import serializers
from clients.models import Client
from doctors.models import Doctor, Specialization, Schedule, Slot
from patients.models import *
from appointments.models import Appoinment


class ContactTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['code']


class ClientIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['id']


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = '__all__'


class ChiefComplaintSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChiefComplaint
        fields = '__all__'


class PresentIllnessImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PresentIllnessImage
        fields = '__all__'


class PresentIllnessSerializer(serializers.ModelSerializer):
    class Meta:
        model = PresentIllness
        fields = '__all__'


class ChildhoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChildhoodIllness
        fields = '__all__'


class AdultIllnessSerialzer(serializers.ModelSerializer):
    class Meta:
        model = AdultIllness
        fields = '__all__'


class HistoryOfImmunizationSerialzer(serializers.ModelSerializer):
    class Meta:
        model = HistoryOfImmunization
        fields = '__all__'


class FamilyHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = FamilyHistory
        fields = '__all__'


class PersonalAndSocialHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonalAndSocialHistory
        fields = '__all__'


class FunctionalHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = FunctionalHistory
        fields = '__all__'


class GeneralSystemSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeneralSystem
        fields = '__all__'


class SkinProblemSerializer(serializers.ModelSerializer):
    class Meta:
        model = SkinProblem
        fields = '__all__'


class HeentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Heent
        fields = '__all__'


class BreastSerializer(serializers.ModelSerializer):
    class Meta:
        model = Breast
        fields = '__all__'


class PulmonarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Pulmonary
        fields = '__all__'


class CardiovascularSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cardiovascular
        fields = '__all__'


class GastrointestinalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gastrointestinal
        fields = '__all__'


class GenitourinarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Genitourinary
        fields = '__all__'


class GynecologicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gynecologic
        fields = '__all__'


class EndocrineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Endocrine
        fields = '__all__'


class MusculoskeletalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Musculoskeletal
        fields = '__all__'


class NeurologicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Neurologic
        fields = '__all__'


class SpecializationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialization
        fields = '__all__'


class DoctorSerializer(serializers.ModelSerializer):
    specialization = SpecializationSerializer(many=False)

    class Meta:
        model = Doctor
        fields = '__all__'


# class PatientCheckupSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = PatientCheckup
#         fields = '__all__'


class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = '__all__'

    def to_representation(self, instance):
        representation = super(
            ScheduleSerializer, self).to_representation(instance)
        representation['start'] = instance.start.strftime('%I:%M %p')
        representation['end'] = instance.end.strftime('%I:%M %p')
        return representation


class SlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slot
        fields = '__all__'


class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appoinment
        fields = '__all__'

    def to_representation(self, instance):
        representation = super(
            AppointmentSerializer, self).to_representation(instance)
        representation['created_at'] = instance.created_at.strftime(
            '%B %d, %Y - %I:%M %p')
        if representation['checkup_date'] is not None:
            # representation['checkup_date'] = instance.checkup_date.strftime(
            #     '%B %d, %Y')
            representation['checkup_start'] = instance.checkup_start.strftime(
                '%I:%M %p')
            representation['checkup_end'] = instance.checkup_end.strftime(
                '%I:%M %p')
        return representation
