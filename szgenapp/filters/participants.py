import django_filters

from szgenapp.models.participants import StudyParticipant, PARTICIPANT_STATUS_CHOICES, COUNTRY_CHOICES


class StudyParticipantFilter(django_filters.FilterSet):
    country = django_filters.MultipleChoiceFilter(choices=COUNTRY_CHOICES, field_name='country')
    status = django_filters.MultipleChoiceFilter(choices=PARTICIPANT_STATUS_CHOICES, field_name='status')
    alphacode = django_filters.CharFilter(field_name='alphacode')
    secondaryid = django_filters.CharFilter(field_name='secondaryid')
    accessid = django_filters.CharFilter(field_name='accessid', lookup_expr='icontains')
    npid = django_filters.CharFilter(field_name='npid')
    fullnumber__contains = django_filters.CharFilter('fullnumber', lookup_expr='icontains')
    fullnumber__exact = django_filters.CharFilter('fullnumber', lookup_expr='exact')

    class Meta:
        model = StudyParticipant
        fields = ['fullnumber__exact', 'fullnumber__contains', 'country', 'study', 'status', 'accessid','alphacode', 'secondaryid', 'npid', 'family',
                  'individual', 'district']
