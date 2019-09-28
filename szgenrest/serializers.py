from rest_framework import serializers

from szgenapp.models import Study, StudyParticipant, Clinical, Sample, Dataset, SubSample, Location
from szgenapp.models.clinical import Demographic, Diagnosis, MedicalHistory, SymptomsMania, SymptomsDepression, \
    SymptomsBehaviour, SymptomsHallucination, SymptomsDelusion, SymptomsGeneral


class StudySerializer(serializers.ModelSerializer):
    class Meta:
        model = Study
        fields = ('id', 'title', 'precursor', 'description', 'status', 'notes')


class StudyParticipantSerializer(serializers.ModelSerializer):
    study = StudySerializer()
    class Meta:
        model = StudyParticipant
        fields = '__all__'


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'


class SubSampleSerializer(serializers.ModelSerializer):
    location = LocationSerializer()

    class Meta:
        model = SubSample
        fields = '__all__'


class SampleSerializer(serializers.ModelSerializer):
    participant = StudyParticipantSerializer()
    sample_types = serializers.StringRelatedField(many=True)
    subsamples = SubSampleSerializer(many=True, read_only=True)

    class Meta:
        model = Sample
        fields = ('id', 'participant', 'sample_types', 'rebleed', 'arrival_date', 'subsamples')


class DatasetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dataset
        fields = '__all__'


class DemographicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Demographic
        fields = '__all__'


class DiagnosisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Diagnosis
        fields = '__all__'


class MedicalHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalHistory
        fields = '__all__'


class SymptomsGeneralSerializer(serializers.ModelSerializer):
    class Meta:
        model = SymptomsGeneral
        fields = '__all__'


class SymptomsDelusionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SymptomsDelusion
        fields = '__all__'


class SymptomsHallucinationSerializer(serializers.ModelSerializer):
    class Meta:
        model = SymptomsHallucination
        fields = '__all__'


class SymptomsBehaviourSerializer(serializers.ModelSerializer):
    class Meta:
        model = SymptomsBehaviour
        fields = '__all__'


class SymptomsDepressionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SymptomsDepression
        fields = '__all__'


class SymptomsManiaSerializer(serializers.ModelSerializer):
    class Meta:
        model = SymptomsMania
        fields = '__all__'


class ClinicalSerializer(serializers.ModelSerializer):
    participant = StudyParticipantSerializer()
    demographic = DemographicSerializer()
    diagnosis = DiagnosisSerializer()
    medicalhistory = MedicalHistorySerializer()
    symptomsgeneral = SymptomsGeneralSerializer()
    symptomsdelusion = SymptomsDelusionSerializer()
    symptomshallucination = SymptomsHallucinationSerializer()
    symptomsbehaviour = SymptomsBehaviourSerializer()
    symptomsdepression = SymptomsDepressionSerializer()
    symptomsmania = SymptomsManiaSerializer()

    class Meta:
        model = Clinical
        fields = (
        'id', 'participant', 'demographic', 'diagnosis', 'medicalhistory', 'symptomsgeneral', 'symptomsdelusion',
        'symptomshallucination', 'symptomsbehaviour', 'symptomsdepression', 'symptomsmania')
