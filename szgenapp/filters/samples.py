import django_filters
from django_filters.widgets import RangeWidget, SuffixedMultiWidget
from django import forms
from szgenapp.models.samples import Sample, SubSample
from szgenapp.models.studies import Study

class DurationRangeWidget(RangeWidget):

    def __init__(self, attrs=None):
        super().__init__(attrs)
        self.widgets[0].attrs.update({'class': 'datepicker', 'placeholder': 'from'})
        self.widgets[1].attrs.update({'class': 'datepicker', 'placeholder': 'to'})

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


class SampleFilter(django_filters.FilterSet):
    participant = django_filters.CharFilter(field_name='participant__fullnumber',
                                            lookup_expr='icontains', label='Participant Full Number'
                                            )
    study = django_filters.ModelChoiceFilter(
        field_name='participant__study', label='Study',
        queryset=Study.objects.all())

    notes = django_filters.CharFilter(field_name='notes', lookup_expr='icontains', label='Notes')
    arrival_date = django_filters.DateFromToRangeFilter(field_name='arrival_date', label='Arrival date from/to',
                                                        widget=DurationRangeWidget)

    class Meta:
        model = Sample
        fields = ['participant', 'study', 'arrival_date', 'sample_type', 'rebleed', 'notes']


class SubSampleListFilter(django_filters.FilterSet):
    participant = django_filters.CharFilter(field_name='sample__participant__fullnumber',
                                            lookup_expr='icontains', label='Participant Full Number'
                                            )
    study = django_filters.ModelChoiceFilter(
        field_name='sample__participant__study', label='Study',
        queryset=Study.objects.all())

    notes = django_filters.CharFilter(field_name='notes', lookup_expr='icontains', label='Notes')

    class Meta:
        model = SubSample
        fields = ['participant', 'study', 'sample_type', 'sample_num', 'storage_date', 'used', 'used_date', 'location', 'notes']