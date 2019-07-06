from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path(r'study/create/', views.StudyCreate.as_view(), name="study_create"),
    path(r'study/<pk>/', views.StudyDetail.as_view(), name="study_detail"),
    path(r'study/update/<pk>/', views.StudyUpdate.as_view(), name="study_update"),
]