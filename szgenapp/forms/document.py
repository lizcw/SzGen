from django.forms import Form, ModelForm, FileField, FileInput, ModelChoiceField, ChoiceField

from szgenapp.models.document import Document
from szgenapp.models.studies import Study


class DocumentForm(ModelForm):
    docfile = FileField()

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     for field in iter(self.fields):
    #         self.fields[field].widget.attrs.update({
    #             'class': 'form-control'
    #         })

    class Meta:
        model = Document
        fields = ('docfile', 'description', 'study')
        exclude = ['doctype']
        widgets = {
            'docfile': FileInput()
        }


class ImportForm(Form):
    DATA_TABLES = (('Dataset', 'Dataset'), ('Study', 'Study'), ('Participant', 'Participant'), ('Clinical', 'Clinical'), ('Sample', 'Sample'))
    document = ModelChoiceField(queryset=Document.objects.filter(doctype__in=['.csv']))
    datatable = ChoiceField(choices=DATA_TABLES)
    study = ModelChoiceField(queryset=Study.objects.all(), required=False)

    class Meta:
        fields = ['document', 'datatable', 'study']
