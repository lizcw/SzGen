import logging

from django.db import IntegrityError, transaction
from django.urls import reverse
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView
from django_filters.views import FilterView
from django_tables2.export.views import ExportMixin
from django_tables2.views import SingleTableMixin

from szgenapp.filters.samples import *
from szgenapp.forms.samples import SampleForm, SubSampleForm, \
    LocationFormset, TransformSampleForm, HarvestSampleForm, \
    ShipmentForm, QCForm
from szgenapp.models.samples import HarvestSample, TransformSample, SAMPLE_TYPES, SUBSAMPLE_TYPES, Shipment, SampleType, \
    Location, QC
from szgenapp.tables import *

logger = logging.getLogger(__name__)


class SampleDetail(DetailView):
    """
    View details of a blood sample
    """
    model = Sample
    template_name = 'sample/sample.html'
    context_object_name = 'sample'

    def get_context_data(self, **kwargs):
        data = super(SampleDetail, self).get_context_data(**kwargs)
        sample = data['sample']
        if sample:
            data['subsampletypes'] = SUBSAMPLE_TYPES
            data['LCYTE'] = sample.subsample_set.filter(sample_type='LCYTE')
            data['LCL'] = sample.subsample_set.filter(sample_type='LCL')
            data['DNA'] = sample.subsample_set.filter(sample_type='DNA')
        return data


class SampleDelete(DeleteView):
    """
    Delete a Sample and all subsamples
    """
    model = Sample
    template_name = 'sample/sample-confirm-delete.html'

    def get_success_url(self):
        return reverse('participant_detail', args=[self.object.participant.id])


class SampleParticipantCreate(CreateView):
    """
    Enter Sample data for new Sample with Participant
    ONLY sample fields here - subsamples created with their own forms
    """
    model = Sample
    template_name = 'sample/sample-create.html'
    form_class = SampleForm

    def get_initial(self, *args, **kwargs):
        initial = super(SampleParticipantCreate, self).get_initial(**kwargs)
        if self.kwargs.get('participantid'):
            pid = self.kwargs.get('participantid')
            initial['participant'] = StudyParticipant.objects.get(pk=pid)
        return initial

    def get_context_data(self, **kwargs):
        data = super(SampleParticipantCreate, self).get_context_data(**kwargs)
        pid = self.kwargs.get('participantid')
        participant = StudyParticipant.objects.get(pk=pid)
        data['subtitle'] = 'Create Sample for %s' % participant
        data['participant'] = participant
        return data

    def get_success_url(self):
        return reverse('sample_detail', args=[self.object.id])


class SampleUpdate(UpdateView):
    """
    Update Sample data for new Sample
    ONLY sample fields here - subsamples created with their own forms
    Filter Participant list or will try to load all participants
    """
    model = Sample
    template_name = 'sample/sample-create.html'
    form_class = SampleForm
    context_object_name = 'sample'

    def get_initial(self, *args, **kwargs):
        initial = super(SampleUpdate, self).get_initial(**kwargs)
        initial['participant'] = self.object.participant
        return initial

    def get_context_data(self, **kwargs):
        data = super(SampleUpdate, self).get_context_data(**kwargs)
        data['subtitle'] = 'Update Sample for %s' % self.get_object().participant
        return data

    def get_success_url(self):
        return reverse('sample_detail', args=[self.object.id])


class SampleList(SingleTableMixin, ExportMixin, FilterView):
    """
    List of Samples - filterable by study
    """
    model = Sample
    template_name = 'sample/sample-list.html'
    queryset = Sample.objects.all()
    context_object_name = 'samples'
    filterset_class = SampleFilter
    table_class = SampleTable

    def get_context_data(self, *args, **kwargs):
        initial = super(SampleList, self).get_context_data(*args, **kwargs)
        initial['collections'] = SAMPLE_TYPES
        initial['subcollections'] = SUBSAMPLE_TYPES
        sampletype = self.kwargs.get('sampletype')
        if sampletype is None:
            initial['title'] = 'All'
            initial['reset_url'] = reverse('samples')
        else:
            initial['title'] = [x[1] for x in SAMPLE_TYPES if x[0] == sampletype][0]
            initial['reset_url'] = '/samples/%s' % sampletype
        study = self.kwargs.get('study')
        if study is not None:
            initial['title'] += " for " + study
        return initial

    def get_queryset(self):
        sampletype = self.kwargs.get('sampletype')
        study = self.kwargs.get('study')
        qs = Sample.objects.all()
        if study is not None:
            qs = qs.filter(participant__study__id=study)
        if sampletype is not None:
            qs = SampleType.objects.get(name__iexact=sampletype).sample_set.all()

        return qs


class SubSampleList(SingleTableMixin, ExportMixin, FilterView):
    """
    List of subsample by type
    """
    model = SubSample
    template_name = 'sample/sample-list.html'
    filterset_class = SubSampleListFilter
    table_class = SubSampleTable

    def get_context_data(self, *args, **kwargs):
        initial = super(SubSampleList, self).get_context_data(*args, **kwargs)
        initial['collections'] = SAMPLE_TYPES
        initial['subcollections'] = SUBSAMPLE_TYPES
        sampletype = self.kwargs.get('sampletype')
        if sampletype is None:
            initial['title'] = 'All'
        else:
            initial['title'] = [x[1] for x in SUBSAMPLE_TYPES if x[0] == sampletype][0]
        initial['reset_url'] = '/subsample/list/%s' % sampletype
        return initial

    def get_queryset(self):
        sampletype = self.kwargs.get('sampletype')
        if sampletype is None:
            qs = SubSample.objects.all()
        else:
            qs = SubSample.objects.filter(sample_type=sampletype)

        return qs


"""
SHIPMENT
"""


class ShipmentCreate(CreateView):
    """
    Add Shipment data to new Sample
    """
    model = Shipment
    template_name = 'sample/sample-create.html'
    form_class = ShipmentForm
    sample = Sample

    def get_initial(self):
        initial = super(ShipmentCreate, self).get_initial()
        self.sample = Sample.objects.get(pk=self.kwargs.get('sampleid'))
        initial['sample'] = self.sample
        return initial

    def get_context_data(self, **kwargs):
        data = super(ShipmentCreate, self).get_context_data(**kwargs)
        data['subtitle'] = 'Create Shipment for %s' % self.sample.participant
        return data

    def get_success_url(self):
        return reverse('sample_detail', args=[self.sample.id])


class ShipmentUpdate(UpdateView):
    """
    Update Shipment data only
    """
    model = Shipment
    template_name = 'sample/sample-create.html'
    form_class = ShipmentForm

    def get_initial(self):
        data = super(ShipmentUpdate, self).get_initial()
        data['sample'] = self.get_object().sample
        return data

    def get_context_data(self, **kwargs):
        data = super(ShipmentUpdate, self).get_context_data(**kwargs)
        data['subtitle'] = 'Update Shipment for %s' % self.object.sample.participant
        return data

    def get_success_url(self):
        return reverse('sample_detail', args=[self.object.sample.id])

class ShipmentDelete(DeleteView):
    """
    Delete shipment
    """
    model = Shipment
    template_name = 'sample/subsample-confirm-delete.html'

    def get_context_data(self, **kwargs):
        data = super(self.__class__, self).get_context_data(**kwargs)
        data['title'] = 'Confirm %s delete' % self.__class__

    def get_success_url(self):
        return reverse('sample_detail', args=[self.object.sample.id])


"""
QUALITY CONTROL
"""


class QCCreate(CreateView):
    """
    Add Shipment data to new Sample
    """
    model = QC
    template_name = 'sample/sample-create.html'
    form_class = QCForm
    sample = Sample

    def get_initial(self):
        initial = super(QCCreate, self).get_initial()
        self.sample = Sample.objects.get(pk=self.kwargs.get('sampleid'))
        initial['sample'] = self.sample
        return initial

    def get_context_data(self, **kwargs):
        data = super(QCCreate, self).get_context_data(**kwargs)
        data['subtitle'] = 'Create QC for %s' % self.sample.participant
        return data

    def get_success_url(self):
        return reverse('sample_detail', args=[self.sample.id])


class QCUpdate(UpdateView):
    """
    Update QC data only
    """
    model = QC
    template_name = 'sample/sample-create.html'
    form_class = QCForm

    def get_initial(self):
        data = super(QCUpdate, self).get_initial()
        data['sample'] = self.get_object().sample
        return data

    def get_context_data(self, **kwargs):
        data = super(QCUpdate, self).get_context_data(**kwargs)
        data['subtitle'] = 'Update QC for %s' % self.object.sample.participant
        return data

    def get_success_url(self):
        return reverse('sample_detail', args=[self.object.sample.id])


class QCDelete(DeleteView):
    """
    Delete QC
    """
    model = QC
    template_name = 'sample/subsample-confirm-delete.html'

    def get_context_data(self, **kwargs):
        data = super(self.__class__, self).get_context_data(**kwargs)
        data['title'] = 'Confirm delete Quality Control for %s' % self.object.sample.participant
        return data

    def get_success_url(self):
        return reverse('sample_detail', args=[self.object.sample.id])

"""
TRANSFORMS
"""


class TransformSampleCreate(CreateView):
    """
    Add Sample Transform data to new Sample
    """
    model = TransformSample
    template_name = 'sample/sample-create.html'
    form_class = TransformSampleForm
    sample = Sample

    def get_initial(self):
        data = super(TransformSampleCreate, self).get_initial()
        sample_id = self.kwargs.get('sampleid')
        self.sample = Sample.objects.get(pk=sample_id)
        data['sample'] = self.sample
        return data

    def get_context_data(self, **kwargs):
        data = super(TransformSampleCreate, self).get_context_data(**kwargs)
        data['subtitle'] = 'Create Transform for %s' % self.sample.participant
        return data

    def get_success_url(self):
        return reverse('sample_detail', args=[self.sample.id])


class TransformSampleUpdate(UpdateView):
    """
    Update TransformSample data only
    """
    model = TransformSample
    template_name = 'sample/sample-create.html'
    form_class = TransformSampleForm

    def get_initial(self):
        data = super(TransformSampleUpdate, self).get_initial()
        data['sample'] = self.get_object().sample
        return data

    def get_context_data(self, **kwargs):
        data = super(TransformSampleUpdate, self).get_context_data(**kwargs)
        data['subtitle'] = 'Update Transform for %s' % self.object.sample.participant
        return data

    def get_success_url(self):
        return reverse('sample_detail', args=[self.object.sample.id])


class TransformSampleDelete(DeleteView):
    """
    Delete transform
    """
    model = TransformSample
    template_name = 'sample/subsample-confirm-delete.html'

    def get_context_data(self, **kwargs):
        data = super(self.__class__, self).get_context_data(**kwargs)
        data['title'] = 'Confirm delete Transform data for %s' % self.object.sample.participant
        return data

    def get_success_url(self):
        return reverse('sample_detail', args=[self.object.sample.id])

"""
HARVESTS
"""


class HarvestSampleCreate(CreateView):
    """
    Add Sample Harvest data to new Sample
    """
    model = HarvestSample
    template_name = 'sample/sample-create.html'
    form_class = HarvestSampleForm
    sample = Sample

    def get_initial(self):
        data = super(HarvestSampleCreate, self).get_initial()
        sample_id = self.kwargs.get('sampleid')
        self.sample = Sample.objects.get(pk=sample_id)
        data['sample'] = self.sample
        return data

    def get_context_data(self, **kwargs):
        data = super(HarvestSampleCreate, self).get_context_data(**kwargs)
        data['subtitle'] = 'Create Harvest record for %s' % self.sample.participant
        return data

    def get_success_url(self):
        return reverse('sample_detail', args=[self.sample.id])


class HarvestSampleUpdate(UpdateView):
    """
    Update HarvestSample data only
    """
    model = HarvestSample
    template_name = 'sample/sample-create.html'
    form_class = HarvestSampleForm

    def get_initial(self):
        data = super(HarvestSampleUpdate, self).get_initial()
        data['sample'] = self.get_object().sample
        return data

    def get_context_data(self, **kwargs):
        data = super(HarvestSampleUpdate, self).get_context_data(**kwargs)
        data['subtitle'] = 'Update Harvest record for %s' % self.object.sample.participant
        return data

    def get_success_url(self):
        return reverse('sample_detail', args=[self.object.sample.id])

class HarvestSampleDelete(DeleteView):
    """
    Delete Harvest
    """
    model = HarvestSample
    template_name = 'sample/subsample-confirm-delete.html'

    def get_context_data(self, **kwargs):
        data = super(self.__class__, self).get_context_data(**kwargs)
        data['title'] = 'Confirm delete Harvest data for %s' % self.object.sample.participant
        return data

    def get_success_url(self):
        return reverse('sample_detail', args=[self.object.sample.id])

"""
SUBSAMPLES
"""


class SubSampleCreate(CreateView):
    """
    Add subsample of various types: Lymphocyte, LCL, DNA
    """
    model = SubSample
    template_name = 'sample/sample-create.html'
    form_class = SubSampleForm
    sample = Sample
    subtitle = 'Create Subsample'

    def get_initial(self, **kwargs):
        initial = super(SubSampleCreate, self).get_initial(**kwargs)
        sample_id = self.kwargs.get('sampleid')
        sample_type_key = self.kwargs.get('sampletype')
        sample_type = [item for item in SUBSAMPLE_TYPES if item[0] == sample_type_key]
        self.sample = Sample.objects.get(pk=sample_id)
        self.subtitle = 'Create %s storage record for %s Sample' % (sample_type[0][1], self.sample.participant)
        initial['sample'] = self.sample
        initial['sample_type'] = sample_type[0][0]
        initial['sample_num'] = self.sample.get_next_subsample_num(sample_type[0][1])
        return initial

    def get_context_data(self, **kwargs):
        data = super(SubSampleCreate, self).get_context_data(**kwargs)
        data['subtitle'] = self.subtitle
        data['sample'] = self.sample
        if self.request.POST:
            data['location'] = LocationFormset(self.request.POST)
        else:
            data['location'] = LocationFormset()
        return data

    def form_valid(self, form):
        try:
            context = self.get_context_data()
            location = context['location']
            # Save new location then add to storage_location
            with transaction.atomic():
                self.object = form.save()

            if location.is_valid():
                subsample_location = location.save()
                self.object.location = subsample_location

            self.object.save()
            return super(SubSampleCreate, self).form_valid(form)
        except IntegrityError as e:
            msg = 'Database Error: Unable to create Sample - see Administrator: %s' % e
            form.add_error(None, msg)
            logger.error(msg)
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse('sample_detail', args=[self.sample.id])


class SubSampleUpdate(UpdateView):
    """
    Update Sample data for new Sample
    """
    model = SubSample
    template_name = 'sample/sample-create.html'
    form_class = SubSampleForm

    def get_initial(self, **kwargs):
        initial = super(SubSampleUpdate, self).get_initial(**kwargs)
        if self.kwargs:
            initial['sample'] = self.object.sample
            initial['sample_type'] = self.object.sample_type
        return initial

    def get_context_data(self, **kwargs):
        data = super(SubSampleUpdate, self).get_context_data(**kwargs)
        sampletype = self.get_object().get_sample_type_display()
        data['subtitle'] = 'Update %s storage record for %s Sample' % (
            sampletype, self.get_object().sample.participant)
        data['sample'] = self.get_object().sample
        if self.request.POST:
            data['location'] = LocationFormset(self.request.POST)
        else:
            data['location'] = LocationFormset(instance=self.get_object().location)
        return data

    def form_valid(self, form):
        try:
            context = self.get_context_data()
            location = context['location']
            # Save new location then add to storage_location
            with transaction.atomic():
                self.object = form.save()
            if location.is_valid():
                subsample_location = location.save()
                self.object.location = subsample_location
            self.object.save()
            return super(SubSampleUpdate, self).form_valid(form)
        except IntegrityError as e:
            msg = 'Database Error: Unable to update SubSample - see Administrator: %s' % e
            form.add_error(None, msg)
            logger.error(msg)
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse('sample_detail', args=[self.object.sample.id])

class SubSampleDelete(DeleteView):
    """
    Delete SubSample
    """
    model = SubSample
    template_name = 'sample/subsample-confirm-delete.html'

    def get_context_data(self, **kwargs):
        data = super(self.__class__, self).get_context_data(**kwargs)
        data['title'] = 'Confirm delete %s data for %s' % (
            self.get_object().get_sample_type_display(), self.object.sample.participant)
        return data

    def get_success_url(self):
        return reverse('sample_detail', args=[self.object.sample.id])
