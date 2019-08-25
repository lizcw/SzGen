import django_filters

from szgenapp.models.datasets import Dataset, DatasetFile, DatasetRow, FIELD_TYPES, FILE_CODES, FILE_TYPES


class DatasetFilter(django_filters.FilterSet):
    class Meta:
        model = Dataset
        fields = {'group': ['icontains']}


class DatasetFileFilter(django_filters.FilterSet):
    dataset = django_filters.CharFilter(field_name='dataset__group', lookup_expr='icontains', label='Group contains')
    location = django_filters.CharFilter(field_name='location', lookup_expr='icontains')
    class Meta:
        model = DatasetFile
        fields = '__all__'


class DatasetParticipantFilter(django_filters.FilterSet):
    participant = django_filters.CharFilter(field_name='participant', lookup_expr='icontains')
    dataset = django_filters.CharFilter(field_name='dataset__group', lookup_expr='icontains', label='Group')

    class Meta:
        model = DatasetRow
        fields = '__all__'
        exclude = []
