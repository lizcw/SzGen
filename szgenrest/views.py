from django.shortcuts import render
from rest_framework import viewsets, mixins
from szgenrest.serializers import StudySerializer, StudyParticipantSerializer, ClinicalSerializer, SampleSerializer, DatasetSerializer
from szgenapp.models import Study, StudyParticipant, Clinical, Sample, SubSample, Dataset
from szgenapp.filters import ClinicalFilter, StudyParticipantFilter, SampleFilter

#################################################################################
#
# REST API
#################################################################################

class StudyViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    API endpoint that allows objects to be viewed.
    """
    queryset = Study.objects.all().order_by('title')
    serializer_class = StudySerializer


class ParticipantViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    API endpoint that allows objects to be viewed.
    """
    queryset = StudyParticipant.objects.all().order_by('fullnumber')
    serializer_class = StudyParticipantSerializer
    filter_class = StudyParticipantFilter


class ClinicalViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    API endpoint that allows objects to be viewed.
    """
    queryset = Clinical.objects.all().order_by('participant__fullnumber')
    serializer_class = ClinicalSerializer
    filter_class = ClinicalFilter


class SampleViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    API endpoint that allows objects to be viewed.
    """
    queryset = Sample.objects.all().order_by('participant__fullnumber')
    serializer_class = SampleSerializer
    filter_class = SampleFilter

class DatasetViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    API endpoint that allows objects to be viewed.
    """
    queryset = Dataset.objects.all().order_by('pk')
    serializer_class = DatasetSerializer