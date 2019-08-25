import django_filters

from szgenapp.models.participants import StudyParticipant, PARTICIPANT_STATUS_CHOICES, COUNTRY_CHOICES


class StudyParticipantFilter(django_filters.FilterSet):
    country = django_filters.MultipleChoiceFilter(choices=COUNTRY_CHOICES, field_name='participant__country')
    status = django_filters.MultipleChoiceFilter(choices=PARTICIPANT_STATUS_CHOICES, field_name='participant__status')
    alphacode = django_filters.CharFilter(field_name='participant__alphacode')
    secondaryid = django_filters.CharFilter(field_name='participant__secondaryid')
    npid = django_filters.CharFilter(field_name='participant__npid')
    fullnumber = django_filters.CharFilter('fullnumber', lookup_expr='icontains')

    class Meta:
        model = StudyParticipant
        fields = ['fullnumber', 'country', 'study', 'status', 'alphacode', 'secondaryid', 'npid', 'family',
                  'individual', 'district']
