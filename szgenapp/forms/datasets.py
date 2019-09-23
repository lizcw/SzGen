from django.forms import ModelForm, HiddenInput
from django.forms import ModelForm, HiddenInput
from django.forms.models import inlineformset_factory

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

    def __init__(self, *args, **kwargs):
        super(DatasetRowForm, self).__init__(*args, **kwargs)
        init = kwargs.get('initial')
        if init is not None:
            p = init.get('participant')
            if p is not None:
                self.fields['participant'].queryset = StudyParticipant.objects.filter(pk=p.id)
            else:
                self.fields['participant'].queryset = StudyParticipant.objects.order_by('fullnumber')

    class Meta:
        model = DatasetRow
        fields = '__all__'


DatasetFileFormset = inlineformset_factory(Dataset, DatasetFile, form=DatasetFileForm, extra=1)
DatasetParticipantFormset = inlineformset_factory(Dataset, DatasetRow, form=DatasetRowForm, extra=1)
