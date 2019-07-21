from django.forms import ModelForm, formset_factory, modelformset_factory, modelform_factory
from django.forms.models import BaseInlineFormSet, inlineformset_factory

from szgenapp.models.samples import Sample, SubSample, Shipment, HarvestSample, TransformSample, Location


class SampleForm(ModelForm):
    class Meta:
        model = Sample
        exclude = ['storage_location']


class SubSampleForm(ModelForm):
    class Meta:
        model = SubSample
        exclude = ['location']


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

LocationFormset = modelform_factory(Location, form=LocationForm)

