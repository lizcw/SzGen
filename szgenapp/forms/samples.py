from django.forms import ModelForm, modelform_factory
from django.forms.models import inlineformset_factory

from szgenapp.models.samples import Sample, SubSample, Shipment, HarvestSample, TransformSample, Location, QC
from szgenapp.models.participants import StudyParticipant


class SampleForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(SampleForm, self).__init__(*args, **kwargs)
        if hasattr(kwargs.get('initial'), 'participant'):
            pid = kwargs.get('initial')['participant'].id
            self.fields['participant'].queryset = StudyParticipant.objects.filter(pk=pid)

    class Meta:
        model = Sample
        exclude = ['storage_location']


class SubSampleForm(ModelForm):
    class Meta:
        model = SubSample
        exclude = ['location']
        fields = ['sample', 'sample_num', 'sample_type', 'storage_date',
                  'extraction_date', 'notes', 'used']

    def __init__(self, *args, **kwargs):
        self.sample = kwargs.get('sampleid')
        super(SubSampleForm, self).__init__(*args, **kwargs)


class ShipmentForm(ModelForm):
    class Meta:
        model = Shipment
        fields = '__all__'


class HarvestSampleForm(ModelForm):
    class Meta:
        model = HarvestSample
        fields = '__all__'


class TransformSampleForm(ModelForm):
    class Meta:
        model = TransformSample
        fields = '__all__'


class LocationForm(ModelForm):
    class Meta:
        model = Location
        fields = '__all__'


class QCForm(ModelForm):
    class Meta:
        model = QC
        fields = '__all__'


LocationFormset = modelform_factory(Location, form=LocationForm)
ShipmentFormset = inlineformset_factory(Sample, Shipment, form=ShipmentForm, extra=1)
HarvestFormset = inlineformset_factory(Sample, HarvestSample, form=HarvestSampleForm, extra=1)
TransformFormset = inlineformset_factory(Sample, TransformSample, form=TransformSampleForm, extra=1)
QCFormset = inlineformset_factory(SubSample, QC, form=QCForm, extra=1)
