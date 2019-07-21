from django import forms
from django.forms import ModelForm, Form, ChoiceField
from django.forms.models import BaseInlineFormSet, inlineformset_factory
from szgenapp.models.datasets import DatasetRow, Dataset, DatasetFile


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

    class Meta:
        model = DatasetRow
        fields = '__all__'

DatasetFileFormset = inlineformset_factory(Dataset, DatasetFile, form=DatasetFileForm, extra=1)
DatasetParticipantFormset = inlineformset_factory(Dataset, DatasetRow, form=DatasetRowForm, extra=1)
