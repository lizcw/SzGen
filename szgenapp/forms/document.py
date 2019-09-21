from django.forms import Form, ModelForm, FileField, FileInput, ModelChoiceField, ChoiceField

from szgenapp.models.document import Document
from szgenapp.models.studies import Study


class DocumentForm(ModelForm):
    docfile = FileField()

    class Meta:
        model = Document
        fields = ('docfile', 'description', 'study')
        exclude = ['doctype']
        widgets = {
            'docfile': FileInput()
        }


class ImportForm(Form):
    DATA_TABLES = (('Dataset', 'Dataset'), ('Study', 'Study'), ('Participant', 'Participant'), ('Clinical', 'Clinical'), ('Sample', 'Sample'))
    document = ModelChoiceField(queryset=Document.objects.filter(doctype__in=['.csv']),
                                help_text="Select the data file to import from")
    datatable = ChoiceField(choices=DATA_TABLES, help_text="Select the table to load the data into")

    class Meta:
        fields = ['document', 'datatable']
