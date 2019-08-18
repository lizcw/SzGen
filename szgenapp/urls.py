from django.urls import path, include
from szgenapp.views import *

urlpatterns = [
    path('', studies.index, name='index'),
    path('study/<int:pk>/', studies.StudyDetail.as_view(), name="study_detail"),
    path('study/create/', studies.StudyCreate.as_view(), name="study_create"),
    path('study/update/<int:pk>/', studies.StudyUpdate.as_view(), name="study_update"),
    path('participants/', participants.ParticipantList.as_view(), name="participants"),
    path('participant/<int:pk>/', participants.ParticipantDetail.as_view(), name="participant_detail"),
    path('participant/create/', participants.ParticipantCreate.as_view(), name="participant_create"),
    path('participant/update/<int:pk>/', participants.ParticipantUpdate.as_view(), name="participant_update"),
    path('studyparticipants/', participants.StudyParticipantList.as_view(), name="study_participants"),
    path('studyparticipant/<int:pk>/', participants.StudyParticipantDetail.as_view(), name="study_participant_detail"),
    path('studyparticipant/create/<int:participantid>/', participants.StudyParticipantCreate.as_view(), name="study_participant_create"),
    path('studyparticipant/update/<int:pk>/', participants.StudyParticipantUpdate.as_view(),
         name="studyparticipant_update"),
    path('datasets/', datasets.DatasetList.as_view(), name="datasets"),
    path('dataset/<int:pk>/', datasets.DatasetDetail.as_view(), name="dataset_detail"),
    path('dataset/create/', datasets.DatasetCreate.as_view(), name="dataset_create"),
    path('dataset/row/create/<int:participantid>', datasets.DatasetRowCreate.as_view(), name='datasetrow_create'),
    path('dataset/update/<int:pk>/', datasets.DatasetUpdate.as_view(), name="dataset_update"),
    path('dataset/participants/update/<int:pk>', datasets.DatasetParticipantUpdate.as_view(),
         name='dataset_participants_update'),
    path('samples/', samples.SampleList.as_view(), name="samples"),
    path('sample/<int:pk>/', samples.SampleDetail.as_view(), name="sample_detail"),
    path('sample/create/', samples.SampleCreate.as_view(), name="sample_create"),
    path('sample/create/participant/<int:participantid>/', samples.SampleParticipantCreate.as_view(), name="sample_participant_create"),
    path('sample/update/<int:pk>/', samples.SampleUpdate.as_view(), name="sample_update"),
    path('sample/transform/create/<int:sampleid>/', samples.TransformSampleCreate.as_view(), name="sample_transform_add"),
    path('sample/harvest/create/<int:sampleid>/', samples.HarvestSampleCreate.as_view(), name="sample_harvest_add"),
    path('sample/shipment/create/<int:sampleid>/', samples.ShipmentCreate.as_view(), name="sample_shipment_add"),
    path('sample/transform/update/<int:pk>/', samples.TransformSampleUpdate.as_view(), name="sample_transform_update"),
    path('sample/harvest/update/<int:pk>/', samples.HarvestSampleUpdate.as_view(), name="sample_harvest_update"),
    path('sample/shipment/update/<int:pk>/', samples.ShipmentUpdate.as_view(), name="sample_shipment_update"),
    path('subsample/create/<slug:sampletype>/<int:sampleid>/', samples.SubSampleCreate.as_view(), name="subsample_add"),
    path('subsample/update/<int:pk>/', samples.SubSampleUpdate.as_view(), name="subsample_update"),
    path('clinical/', clinical.ClinicalList.as_view(), name="clinical_list"),
    path('clinical/create/', clinical.ClinicalCreate.as_view(), name="clinical_create"),
    path('clinical/update/<int:pk>', clinical.ClinicalUpdate.as_view(), name="clinical_update"),
    path('clinical/<int:pk>', clinical.ClinicalDetail.as_view(), name="clinical_detail"),
    path('clinical/demographic/', clinical.ClinicalDemographicList.as_view(),
         name='clinical_demographic_list'),
    path('clinical/demographic/create/<int:clinicalid>', clinical.ClinicalDemographicCreate.as_view(),
         name='clinical_demographic_create'),
    path('clinical/demographic/update/<int:pk>', clinical.ClinicalDemographicUpdate.as_view(),
         name='clinical_demographic_update'),
    path('clinical/diagnosis/', clinical.ClinicalDiagnosisList.as_view(), name='clinical_diagnosis_list'),
    path('clinical/diagnosis/create/<int:clinicalid>', clinical.ClinicalDiagnosisCreate.as_view(),
         name='clinical_diagnosis_create'),
    path('clinical/diagnosis/update/<int:pk>', clinical.ClinicalDiagnosisUpdate.as_view(),
         name='clinical_diagnosis_update'),
    path('clinical/medical/', clinical.ClinicalMedicalList.as_view(),
         name='clinical_medical_list'),
    path('clinical/medical/create/<int:clinicalid>', clinical.ClinicalMedicalCreate.as_view(),
         name='clinical_medical_create'),
    path('clinical/medical/update/<int:pk>', clinical.ClinicalMedicalUpdate.as_view(),
         name='clinical_medical_update'),
    path('clinical/symptoms_general/', clinical.ClinicalSymptomsGeneralList.as_view(),
         name='clinical_symptoms_general_list'),
    path('clinical/symptoms_general/create/<int:clinicalid>', clinical.ClinicalSymptomsGeneralCreate.as_view(),
         name='clinical_symptoms_general_create'),
    path('clinical/symptoms_general/update/<int:pk>', clinical.ClinicalSymptomsGeneralUpdate.as_view(),
         name='clinical_symptoms_general_update'),
    path('clinical/symptoms_delusion/', clinical.ClinicalSymptomsDelusionList.as_view(),
         name='clinical_symptoms_delusion_list'),
    path('clinical/symptoms_delusion/create/<int:clinicalid>', clinical.ClinicalSymptomsDelusionCreate.as_view(),
         name='clinical_symptoms_delusion_create'),
    path('clinical/symptoms_delusion/update/<int:pk>', clinical.ClinicalSymptomsDelusionUpdate.as_view(),
         name='clinical_symptoms_delusion_update'),
    path('clinical/symptoms_hallucination/', clinical.ClinicalSymptomsHallucinationList.as_view(),
         name='clinical_symptoms_hallucination_list'),
    path('clinical/symptoms_hallucination/create/<int:clinicalid>', clinical.ClinicalSymptomsHallucinationCreate.as_view(),
         name='clinical_symptoms_hallucination_create'),
    path('clinical/symptoms_hallucination/update/<int:pk>', clinical.ClinicalSymptomsHallucinationUpdate.as_view(),
         name='clinical_symptoms_hallucination_update'),
    path('clinical/symptoms_behaviour/', clinical.ClinicalSymptomsBehaviourList.as_view(),
         name='clinical_symptoms_behaviour_list'),
    path('clinical/symptoms_behaviour/create/<int:clinicalid>', clinical.ClinicalSymptomsBehaviourCreate.as_view(),
         name='clinical_symptoms_behaviour_create'),
    path('clinical/symptoms_behaviour/update/<int:pk>', clinical.ClinicalSymptomsBehaviourUpdate.as_view(),
         name='clinical_symptoms_behaviour_update'),
    path('clinical/symptoms_depression/', clinical.ClinicalSymptomsDepressionList.as_view(),
        name='clinical_symptoms_depression_list'),
    path('clinical/symptoms_depression/create/<int:clinicalid>', clinical.ClinicalSymptomsDepressionCreate.as_view(),
         name='clinical_symptoms_depression_create'),
    path('clinical/symptoms_depression/update/<int:pk>', clinical.ClinicalSymptomsDepressionUpdate.as_view(),
         name='clinical_symptoms_depression_update'),
    path('clinical/symptoms_mania/', clinical.ClinicalSymptomsManiaList.as_view(),
        name='clinical_symptoms_mania_list'),
    path('clinical/symptoms_mania/create/<int:clinicalid>', clinical.ClinicalSymptomsManiaCreate.as_view(),
         name='clinical_symptoms_mania_create'),
    path('clinical/symptoms_mania/update/<int:pk>', clinical.ClinicalSymptomsManiaUpdate.as_view(),
         name='clinical_symptoms_mania_update'),


]
