import django_filters
from szgenapp.models.studies import Study
from szgenapp.models.samples import Sample, SubSample

class StudyFilter(django_filters.FilterSet):
    status = django_filters.ModelMultipleChoiceFilter()

    class Meta:
        model = Study
        fields = ['status']

    @property
    def qs(self):
        parent = super(StudyFilter, self).qs
        status = getattr(self.request, 'status', None)
        return parent.filter(status=status)


class SubSampleFilter(django_filters.FilterSet):
    sampletype = django_filters.ModelChoiceFilter()

    class Meta:
        model = SubSample
        fields = ['sample_type']

    @property
    def qs(self):
        parent = super(SubSampleFilter, self).qs
        sampletype = getattr(self.request, 'sample_type', None)
        return parent.filter(sample_type=sampletype)