from django.forms import ModelForm, modelform_factory, HiddenInput
from django.forms.models import inlineformset_factory
from material import *

from szgenapp.models.samples import Sample, SubSample, Shipment, HarvestSample, TransformSample, Location, QC
from szgenapp.models.participants import StudyParticipant


class SampleForm(ModelForm):

    class Meta:
        model = Sample
        exclude = ['storage_location']
        widgets = {'participant': HiddenInput()}


class SubSampleForm(ModelForm):

    def __init__(self, *args, **kwargs):
        sampletype = kwargs.get('initial').get('sample_type')
        is_dna = sampletype == 'DNA'
        super(SubSampleForm, self).__init__(*args, **kwargs)
        if is_dna:
            self.layout = Layout(Row('sample_num'),
                  Row('storage_date', 'extraction_date'),
                  'notes')
        else:
            self.layout = Layout(Row('sample_num', 'used'),
                                 Row('storage_date'),
                                 'notes')


    class Meta:
        model = SubSample
        exclude = ['location']
        fields = ['sample', 'sample_num', 'sample_type', 'storage_date',
                  'extraction_date', 'notes', 'used']
        widgets = {'sample': HiddenInput(), 'sample_type': HiddenInput()}



class ShipmentForm(ModelForm):

    class Meta:
        model = Shipment
        fields = '__all__'
        widgets = {'sample': HiddenInput()}


class HarvestSampleForm(ModelForm):

    class Meta:
        model = HarvestSample
        fields = '__all__'
        widgets = {'sample': HiddenInput()}


class TransformSampleForm(ModelForm):

    class Meta:
        model = TransformSample
        fields = '__all__'
        widgets = {'sample': HiddenInput()}


class LocationForm(ModelForm):
    layout = Layout(Row('tank', 'shelf', 'cell'))
    class Meta:
        model = Location
        fields = '__all__'



class QCForm(ModelForm):
    layout = Layout(Row('qc_date', 'passed'), 'notes')
    class Meta:
        model = QC
        fields = '__all__'
        widgets = {'sample': HiddenInput()}


LocationFormset = modelform_factory(Location, form=LocationForm)
ShipmentFormset = inlineformset_factory(Sample, Shipment, form=ShipmentForm, extra=1)
HarvestFormset = inlineformset_factory(Sample, HarvestSample, form=HarvestSampleForm, extra=1)
TransformFormset = inlineformset_factory(Sample, TransformSample, form=TransformSampleForm, extra=1)
QCFormset = inlineformset_factory(Sample, QC, form=QCForm, extra=1)
