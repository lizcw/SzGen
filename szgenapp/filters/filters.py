import django_filters
from szgenapp.models import Study


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