import django_filters
from szgenapp.models.document import Document, DOC_TYPES


class DocumentFilter(django_filters.FilterSet):
    doctype = django_filters.ChoiceFilter(choices=DOC_TYPES)
    class Meta:
        model = Document
        fields = ['doctype', 'description', 'study']
