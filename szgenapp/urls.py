from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views

from szgenapp.views import *

urlpatterns = [
                  path('', studies.index, name='index'),
                  path('accounts/', include('django.contrib.auth.urls')),
                  path('login/', auth_views.LoginView.as_view(template_name='app/index.html'), name='login'),
                  path('logout/', auth.LogoutView.as_view(), name='logout'),
                  path('locked/', auth.locked_out, name='locked_out'),
                  path('profile/', auth.ProfileView.as_view(), name='profile'),
                  path('app-password-change/', auth_views.PasswordChangeView.as_view(
                      template_name='registration/password_change_form.html',
                      success_url=reverse_lazy('profile')),
                      name='password_change'),
                  path('study/<int:pk>/', studies.StudyDetail.as_view(), name="study_detail"),
                  path('study/create/', studies.StudyCreate.as_view(), name="study_create"),
                  path('study/update/<int:pk>/', studies.StudyUpdate.as_view(), name="study_update"),
                  path('study/delete/<int:pk>/', studies.StudyDelete.as_view(), name="study_delete"),
                  path('participants/', ParticipantList.as_view(), name="participants"),
                  path('participant/<int:pk>/', ParticipantDetail.as_view(), name="participant_detail"),
                  path('participant/create/', ParticipantCreate.as_view(), name="participant_create"),
                  path('participant/update/<int:pk>/', ParticipantUpdate.as_view(), name="participant_update"),
                  path('participant/delete/<int:pk>/', ParticipantDelete.as_view(), name="participant_delete"),
                  path('studyparticipants/', StudyParticipantList.as_view(), name="study_participants"),
                  path('studyparticipant/<int:pk>', StudyParticipantDetail.as_view(),
                       name="study_participant_detail"),
                  path('studyparticipant/create/<int:participantid>/', StudyParticipantCreate.as_view(),
                       name="study_participant_create"),
                  path('studyparticipant/update/<int:pk>/', StudyParticipantUpdate.as_view(),
                       name="study_participant_update"),
                  path('datasets/', datasets.DatasetList.as_view(), name="datasets"),
                  path('dataset/participants/', datasets.DatasetParticipantList.as_view(), name='dataset_participants'),
                  path('dataset/files/', datasets.DatasetFileList.as_view(), name='dataset_files'),
                  path('dataset/<int:pk>/', datasets.DatasetDetail.as_view(), name="dataset_detail"),
                  path('dataset/create/', datasets.DatasetCreate.as_view(), name="dataset_create"),
                  path('dataset/update/<int:pk>/', datasets.DatasetUpdate.as_view(), name="dataset_update"),
                  path('dataset/delete/<int:pk>/', datasets.DatasetDelete.as_view(), name="dataset_delete"),
                  path('dataset/row/create/<int:datasetid>/', datasets.DatasetRowCreate.as_view(),
                       name='dataset_row_create'),
                  path('dataset/row/create/<int:datasetid>/<int:participantid>/', datasets.DatasetRowCreate.as_view(),
                       name='dataset_participant_create'),
                  path('dataset/row/participant/update/<int:pk>/', datasets.DatasetParticipantUpdate.as_view(),
                       name='dataset_participant_update'),
                  path('dataset/files/create/<int:datasetid>', datasets.DatasetFileCreate.as_view(),
                       name='dataset_files_create'),
                  path('dataset/files/update/<int:pk>/', datasets.DatasetFileUpdate.as_view(),
                       name='dataset_files_update'),
                  path('samples/<slug:sampletype>/', SampleList.as_view(), name="sample_list"),
                  path('samples/', SampleList.as_view(), name="samples"),
                  path('sample/<int:pk>/', SampleDetail.as_view(), name="sample_detail"),
                  path('sample/create/', SampleCreate.as_view(), name="sample_create"),
                  path('sample/create/participant/<int:participantid>/', SampleParticipantCreate.as_view(),
                       name="sample_participant_create"),
                  path('sample/update/<int:pk>/', SampleUpdate.as_view(), name="sample_update"),
                  path('sample/delete/<int:pk>/', SampleDelete.as_view(), name="sample_delete"),
                  path('sample/transform/create/<int:sampleid>/', TransformSampleCreate.as_view(),
                       name="sample_transform_add"),
                  path('sample/harvest/create/<int:sampleid>/', HarvestSampleCreate.as_view(),
                       name="sample_harvest_add"),
                  path('sample/shipment/create/<int:sampleid>/', ShipmentCreate.as_view(), name="sample_shipment_add"),
                  path('sample/transform/update/<int:pk>/', TransformSampleUpdate.as_view(),
                       name="sample_transform_update"),
                  path('sample/harvest/update/<int:pk>/', HarvestSampleUpdate.as_view(), name="sample_harvest_update"),
                  path('sample/shipment/update/<int:pk>/', ShipmentUpdate.as_view(), name="sample_shipment_update"),
                  path('subsample/create/<slug:sampletype>/<int:sampleid>/', SubSampleCreate.as_view(),
                       name="subsample_add"),
                  path('subsample/update/<int:pk>/', SubSampleUpdate.as_view(), name="subsample_update"),
                  path('subsample/list/<slug:sampletype>', SubSampleList.as_view(), name="subsample_list"),
                  path('clinical/', ClinicalList.as_view(), name="clinical_list"),
                  path('clinical/create/', ClinicalCreate.as_view(), name="clinical_create"),
                  path('clinical/create/participant/<int:participantid>/', ClinicalCreate.as_view(),
                       name="clinical_participant_create"),
                  path('clinical/update/<int:pk>', ClinicalUpdate.as_view(), name="clinical_update"),
                  path('clinical/delete/<int:pk>', ClinicalDelete.as_view(), name="clinical_delete"),
                  path('clinical/<int:pk>', ClinicalDetail.as_view(), name="clinical_detail"),
                  path('clinical/demographic/', ClinicalDemographicList.as_view(),
                       name='clinical_demographic_list'),
                  path('clinical/demographic/create/<int:clinicalid>/', ClinicalDemographicCreate.as_view(),
                       name='clinical_demographic_create'),
                  path('clinical/demographic/update/<int:pk>/', ClinicalDemographicUpdate.as_view(),
                       name='clinical_demographic_update'),
                  path('clinical/diagnosis/', ClinicalDiagnosisList.as_view(), name='clinical_diagnosis_list'),
                  path('clinical/diagnosis/create/<int:clinicalid>/', ClinicalDiagnosisCreate.as_view(),
                       name='clinical_diagnosis_create'),
                  path('clinical/diagnosis/update/<int:pk>/', ClinicalDiagnosisUpdate.as_view(),
                       name='clinical_diagnosis_update'),
                  path('clinical/medical/', ClinicalMedicalList.as_view(),
                       name='clinical_medical_list'),
                  path('clinical/medical/create/<int:clinicalid>/', ClinicalMedicalCreate.as_view(),
                       name='clinical_medical_create'),
                  path('clinical/medical/update/<int:pk>/', ClinicalMedicalUpdate.as_view(),
                       name='clinical_medical_update'),
                  path('clinical/symptoms_general/', ClinicalSymptomsGeneralList.as_view(),
                       name='clinical_symptoms_general_list'),
                  path('clinical/symptoms_general/create/<int:clinicalid>/', ClinicalSymptomsGeneralCreate.as_view(),
                       name='clinical_symptoms_general_create'),
                  path('clinical/symptoms_general/update/<int:pk>/', ClinicalSymptomsGeneralUpdate.as_view(),
                       name='clinical_symptoms_general_update'),
                  path('clinical/symptoms_delusion/', ClinicalSymptomsDelusionList.as_view(),
                       name='clinical_symptoms_delusion_list'),
                  path('clinical/symptoms_delusion/create/<int:clinicalid>/', ClinicalSymptomsDelusionCreate.as_view(),
                       name='clinical_symptoms_delusion_create'),
                  path('clinical/symptoms_delusion/update/<int:pk>/', ClinicalSymptomsDelusionUpdate.as_view(),
                       name='clinical_symptoms_delusion_update'),
                  path('clinical/symptoms_hallucination/', ClinicalSymptomsHallucinationList.as_view(),
                       name='clinical_symptoms_hallucination_list'),
                  path('clinical/symptoms_hallucination/create/<int:clinicalid>/',
                       ClinicalSymptomsHallucinationCreate.as_view(),
                       name='clinical_symptoms_hallucination_create'),
                  path('clinical/symptoms_hallucination/update/<int:pk>/',
                       ClinicalSymptomsHallucinationUpdate.as_view(),
                       name='clinical_symptoms_hallucination_update'),
                  path('clinical/symptoms_behaviour/', ClinicalSymptomsBehaviourList.as_view(),
                       name='clinical_symptoms_behaviour_list'),
                  path('clinical/symptoms_behaviour/create/<int:clinicalid>/',
                       ClinicalSymptomsBehaviourCreate.as_view(),
                       name='clinical_symptoms_behaviour_create'),
                  path('clinical/symptoms_behaviour/update/<int:pk>/', ClinicalSymptomsBehaviourUpdate.as_view(),
                       name='clinical_symptoms_behaviour_update'),
                  path('clinical/symptoms_depression/', ClinicalSymptomsDepressionList.as_view(),
                       name='clinical_symptoms_depression_list'),
                  path('clinical/symptoms_depression/create/<int:clinicalid>/',
                       ClinicalSymptomsDepressionCreate.as_view(),
                       name='clinical_symptoms_depression_create'),
                  path('clinical/symptoms_depression/update/<int:pk>/', ClinicalSymptomsDepressionUpdate.as_view(),
                       name='clinical_symptoms_depression_update'),
                  path('clinical/symptoms_mania/', ClinicalSymptomsManiaList.as_view(),
                       name='clinical_symptoms_mania_list'),
                  path('clinical/symptoms_mania/create/<int:clinicalid>/', ClinicalSymptomsManiaCreate.as_view(),
                       name='clinical_symptoms_mania_create'),
                  path('clinical/symptoms_mania/update/<int:pk>/', ClinicalSymptomsManiaUpdate.as_view(),
                       name='clinical_symptoms_mania_update'),
                  path('documents/create/', DocumentCreate.as_view(), name="documents_create"),
                  path('documents/<int:pk>/', DocumentDetail.as_view(), name="documents_detail"),
                  path('documents/<int:pk>/update/', DocumentUpdate.as_view(), name="documents_update"),
                  path('documents/<int:pk>/delete/', DocumentDelete.as_view(), name="documents_delete"),
                  path('documents/list/', DocumentList.as_view(), name='documents_list'),
                  path('documents/import/<int:pk>', DocumentImport.as_view(), name='documents_data_import')

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
