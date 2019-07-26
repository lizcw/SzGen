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
    path('studyparticipants/', participants.StudyParticipantList.as_view(), name="studyparticipants"),
    path('studyparticipant/<int:pk>/', participants.StudyParticipantDetail.as_view(), name="studyparticipant_detail"),
    path('studyparticipant/create/<int:participantid>', participants.StudyParticipantCreate.as_view(), name="studyparticipant_create"),
    path('studyparticipant/update/<int:pk>/', participants.StudyParticipantUpdate.as_view(),
         name="studyparticipant_update"),
    path('datasets/', datasets.DatasetList.as_view(), name="datasets"),
    path('dataset/<int:pk>/', datasets.DatasetDetail.as_view(), name="dataset_detail"),
    path('dataset/create/', datasets.DatasetCreate.as_view(), name="dataset_create"),
    path('dataset/update/<int:pk>/', datasets.DatasetUpdate.as_view(), name="dataset_update"),
    path('dataset/participants/update/<int:pk>', datasets.DatasetParticipantUpdate.as_view(),
         name='dataset_participants_update'),
    path('samples/', samples.SampleList.as_view(), name="samples"),
    path('sample/<int:pk>/', samples.SampleDetail.as_view(), name="sample_detail"),
    path('sample/create/', samples.SampleCreate.as_view(), name="sample_create"),
    path('sample/update/<int:pk>/', samples.SampleUpdate.as_view(), name="sample_update"),
    path('sample/transform/create/<int:sampleid>/', samples.TransformSampleCreate.as_view(), name="sample_transform_add"),
    path('sample/harvest/create/<int:sampleid>/', samples.HarvestSampleCreate.as_view(), name="sample_harvest_add"),
    path('sample/subsample/<slug:sampletype>/create/<int:sampleid>/', samples.SubSampleCreate.as_view(), name="subsample_add"),

]
