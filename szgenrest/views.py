from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from szgenapp.filters import ClinicalFilter, StudyParticipantFilter, SampleFilter
from szgenapp.models import Study, StudyParticipant, Clinical, Sample, Dataset
from szgenrest.serializers import StudySerializer, StudyParticipantSerializer, ClinicalSerializer, SampleSerializer, \
    DatasetSerializer, SampleOnlySerializer


#################################################################################
# PERMISSIONS RESTRICTED FOR UPDATE
#################################################################################
class IsSuperUser(IsAdminUser):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)

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
    permission_classes = (IsAuthenticated,)


class ParticipantViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    API endpoint that allows objects to be viewed.
    """
    queryset = StudyParticipant.objects.all().order_by('fullnumber')
    serializer_class = StudyParticipantSerializer
    filter_class = StudyParticipantFilter
    permission_classes = (IsAuthenticated,)


class ClinicalViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    API endpoint that allows objects to be viewed.
    """
    queryset = Clinical.objects.all().order_by('participant__fullnumber')
    serializer_class = ClinicalSerializer
    filter_class = ClinicalFilter
    permission_classes = (IsAuthenticated,)


class SampleViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    API endpoint that allows objects to be viewed.
    """
    queryset = Sample.objects.all().order_by('participant__fullnumber')
    serializer_class = SampleSerializer
    filter_class = SampleFilter
    permission_classes = (IsAuthenticated,)

class SampleUpdateViewSet(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    """
    API endpoint that allows superadmins to update Samples
    """
    queryset = Sample.objects.all()
    serializer_class = SampleOnlySerializer
    filter_class = SampleFilter
    permission_classes = (IsAuthenticated, IsSuperUser,)


class DatasetViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    API endpoint that allows objects to be viewed.
    """
    queryset = Dataset.objects.all().order_by('pk')
    serializer_class = DatasetSerializer
    permission_classes = (IsAuthenticated,)
