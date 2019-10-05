import django_filters
from django_filters.widgets import RangeWidget

from szgenapp.models.samples import Sample, SubSample
from szgenapp.models.studies import Study


class DurationRangeWidget(RangeWidget):

    def __init__(self, attrs=None):
        super().__init__(attrs)
        self.widgets[0].attrs.update({'class': 'datepicker', 'placeholder': 'from'})
        self.widgets[1].attrs.update({'class': 'datepicker', 'placeholder': 'to'})


class SampleFilter(django_filters.FilterSet):
    participant = django_filters.CharFilter(field_name='participant__fullnumber',
                                            lookup_expr='exact', label='Participant Full Number (exact)'
                                            )
    participant__contains = django_filters.CharFilter(field_name='participant__fullnumber',
                                            lookup_expr='icontains', label='Participant Full Number (contains)'
                                            )
    study = django_filters.ModelChoiceFilter(
        field_name='participant__study', label='Study',
        queryset=Study.objects.all())

    notes = django_filters.CharFilter(field_name='notes', lookup_expr='icontains', label='Notes')
    arrival_date = django_filters.DateFromToRangeFilter(field_name='arrival_date', label='Arrival date from/to',
                                                        widget=DurationRangeWidget)

    class Meta:
        model = Sample
        fields = ['participant', 'participant__contains', 'study', 'arrival_date', 'rebleed', 'notes']


class SubSampleListFilter(django_filters.FilterSet):
    participant = django_filters.CharFilter(field_name='sample__participant__fullnumber',
                                            lookup_expr='exact', label='Participant Full Number (exact)'
                                            )
    participant__contains = django_filters.CharFilter(field_name='sample__participant__fullnumber',
                                            lookup_expr='icontains', label='Participant Full Number (contains)'
                                            )
    study = django_filters.ModelChoiceFilter(
        field_name='sample__participant__study', label='Study',
        queryset=Study.objects.all())

    notes__contains = django_filters.CharFilter(field_name='notes', lookup_expr='icontains')
    tank = django_filters.CharFilter(field_name='location__tank')
    shelf = django_filters.CharFilter(field_name='location__shelf')
    cell = django_filters.CharFilter(field_name='location__cell')
    cell__contains = django_filters.CharFilter(field_name='location__cell', lookup_expr='icontains')

    class Meta:
        model = SubSample
        fields = ['participant', 'participant__contains', 'study', 'sample_num', 'storage_date', 'used', 'tank',
                  'shelf', 'cell', 'cell__contains', 'notes__contains']


class SubSampleDNAListFilter(django_filters.FilterSet):
    participant = django_filters.CharFilter(field_name='sample__participant__fullnumber',
                                            lookup_expr='icontains', label='Participant Full Number (exact)'
                                            )
    participant__contains = django_filters.CharFilter(field_name='sample__participant__fullnumber',
                                                      lookup_expr='icontains', label='Participant Full Number (contains)'
                                                      )
    study = django_filters.ModelChoiceFilter(
        field_name='sample__participant__study', label='Study',
        queryset=Study.objects.all())

    notes__contains = django_filters.CharFilter(field_name='notes', lookup_expr='icontains')

    class Meta:
        model = SubSample
        fields = ['participant', 'participant__contains', 'study', 'sample_num', 'storage_date', 'extraction_date', 'notes__contains']
