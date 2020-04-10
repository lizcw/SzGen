from django.forms import ModelForm, CharField
from django.forms.models import inlineformset_factory
from rest_framework.fields import HiddenField

from szgenapp.models.datasets import DatasetRow, Dataset, DatasetFile
from szgenapp.models.participants import StudyParticipant


class DatasetForm(ModelForm):
    """
    Base formset for editing Datasets and Dataset Files
    """

    class Meta:
        model = Dataset
        fields = '__all__'


class DatasetFileForm(ModelForm):
    class Meta:
        model = DatasetFile
        fields = '__all__'


class DatasetRowForm(ModelForm):
    participant_fullnumber = CharField(required=True, min_length=2, max_length=50, strip=True,
                            label="Participant Full Number")


    class Meta:
        model = DatasetRow
        fields = ('participant_fullnumber', 'dataset', 'digs', 'figs', 'narrative', 'records', 'consensus', 'ldps', 'notes')


DatasetFileFormset = inlineformset_factory(Dataset, DatasetFile, form=DatasetFileForm, extra=0)
DatasetParticipantFormset = inlineformset_factory(Dataset, DatasetRow, form=DatasetRowForm, extra=0)
