from django.shortcuts import render
from rest_framework import viewsets
from szgenrest.serializers import StudySerializer
from szgenapp.models import Study
#################################################################################
#
# REST API
#################################################################################
class StudyViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Study.objects.all().order_by('title')
    serializer_class = StudySerializer
