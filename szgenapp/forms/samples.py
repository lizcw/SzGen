from django.forms import ModelForm, formset_factory, modelformset_factory, modelform_factory
from django.forms.models import BaseInlineFormSet, inlineformset_factory

from szgenapp.models.samples import Sample, SubSample, Shipment, HarvestSample, TransformSample, Location, QC


class SampleForm(ModelForm):
    class Meta:
        model = Sample
        exclude = ['storage_location']


class SubSampleForm(ModelForm):
    class Meta:
        model = SubSample
        exclude = ['location']

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
