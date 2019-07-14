from django.urls import path
from szgenapp.views import *

urlpatterns = [
    path('', studies.index, name='index'),
    path(r'study/create/', studies.StudyCreate.as_view(), name="study_create"),
    path(r'study/<pk>/', studies.StudyDetail.as_view(), name="study_detail"),
    path(r'study/update/<pk>/', studies.StudyUpdate.as_view(), name="study_update"),
    path(r'participants/', participants.ParticipantList.as_view(), name="participants"),
    path(r'participant/create/', participants.ParticipantCreate.as_view(), name="participant_create"),
    path(r'participant/<pk>/', participants.ParticipantDetail.as_view(), name="participant_detail"),
    path(r'p/update/<pk>/', participants.ParticipantUpdate.as_view(), name="participant_update"),
]