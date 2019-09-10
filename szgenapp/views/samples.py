from django.db import IntegrityError, transaction
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView, ListView, DeleteView
from django_filters.views import FilterView
from django_tables2.export.views import ExportMixin
from django_tables2.views import SingleTableMixin

from szgenapp.forms.samples import SampleForm, SubSampleForm, \
    LocationFormset, TransformSampleForm, HarvestSampleForm, \
    ShipmentFormset, TransformFormset, HarvestFormset, ShipmentForm, QCFormset
from szgenapp.models.participants import Participant
from szgenapp.models.samples import Sample, SubSample, \
    HarvestSample, TransformSample, SAMPLE_TYPES, SUBSAMPLE_TYPES, Shipment, QC
from szgenapp.filters.samples import *
from szgenapp.tables import *


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


class SampleCreate(CreateView):
    """
    Create a sample - basic fields only
    """
    model = Sample
    template_name = 'sample/sample-create.html'
    form_class = SampleForm

    # def form_valid(self, form):
    #     try:
    #         with transaction.atomic():
    #             self.object = form.save()
    #         return super(SampleCreate, self).form_valid(form)
    #     except IntegrityError as e:
    #         msg = 'Database Error: Unable to create Sample - see Administrator: %s' % e
    #         # form.add_error('sample-create', msg)
    #         return self.form_invalid(form)

    def get_success_url(self):
        return reverse('sample_detail', args=[self.object.id])

class SampleDelete(DeleteView):
    """
    Delete a Sample and all subsamples
    """
    model = Sample
    success_url = reverse_lazy("samples")
    template_name = 'sample/sample-confirm-delete.html'

class SampleParticipantCreate(CreateView):
    """
    Enter Sample data for new Sample
    """
    model = Sample
    template_name = 'sample/sample-create.html'
    form_class = SampleForm

    def get_initial(self, *args, **kwargs):
        studyparticipant = None
        if (self.kwargs):
            pid = self.kwargs.get('participantid')
            participant = Participant.objects.get(pk=pid)
            studyparticipant = participant.studyparticipants.first()  # TODO First of set by default
        initial = super(SampleParticipantCreate, self).get_initial(**kwargs)
        initial['action'] = 'Create'
        initial['participant'] = studyparticipant
        return initial

    def get_context_data(self, **kwargs):
        data = super(SampleParticipantCreate, self).get_context_data(**kwargs)
        data['title'] = 'Create Sample'
        if self.request.POST:
            data['location'] = LocationFormset(self.request.POST)
            data['shipment'] = ShipmentFormset(self.request.POST)
            data['transform'] = TransformFormset(self.request.POST)
            data['harvest'] = HarvestFormset(self.request.POST)
        else:
            data['location'] = LocationFormset()
            data['shipment'] = ShipmentFormset(instance=self.get_object())
            data['transform'] = TransformFormset(instance=self.get_object())
            data['harvest'] = HarvestFormset(instance=self.get_object())
        return data

    def form_valid(self, form):
        try:
            context = self.get_context_data()
            location = context['location']
            shipment = context['shipment']
            transform = context['transform']
            harvest = context['harvest']
            with transaction.atomic():
                self.object = form.save(commit=False)
            if form.initial['participant']:
                self.object.participant = form.initial['participant']
            # Add additional subforms
            if shipment.is_valid():
                shipment.save()
            if transform.is_valid():
                transform.save()
            if harvest.is_valid():
                harvest.save()
            if location.is_valid():
                storage_location = location.save()
                self.object.storage_location = storage_location
            # final commit
            self.object.save()
            return super(SampleParticipantCreate, self).form_valid(form)
        except IntegrityError as e:
            msg = 'Database Error: Unable to create Sample - see Administrator: %s' % e
            # form.add_error('sample-create', msg)
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse('sample_detail', args=[self.object.id])


class SampleUpdate(UpdateView):
    """
    Update Sample data for new Sample
    """
    model = Sample
    template_name = 'sample/sample-create.html'
    form_class = SampleForm

    def form_valid(self, form):
        try:
            return super(SampleUpdate, self).form_valid(form)
        except IntegrityError as e:
            msg = 'Database Error: Unable to update Sample - see Administrator: %s' % e
            form.add_error('Sample-update', msg)
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse('sample_detail', args=[self.object.id])

    def get_initial(self, *args, **kwargs):
        initial = super(SampleUpdate, self).get_initial()
        initial['action'] = 'Edit'
        return initial


class SampleList(SingleTableMixin, ExportMixin, FilterView):
    """
    List of Samples - filterable by study
    """
    model = Sample
    template_name = 'sample/sample-list.html'
    queryset = Sample.objects.all()
    context_object_name = 'samples'
    # paginate_by = 10
    filterset_class = SampleFilter
    table_class = SampleTable
    # collections = SAMPLE_TYPES
    # ordering = ['']

    def get_context_data(self, *args, **kwargs):
        initial = super(SampleList, self).get_context_data(*args, **kwargs)
        initial['collections'] = SAMPLE_TYPES
        initial['subcollections'] = SUBSAMPLE_TYPES
        sampletype = self.kwargs.get('sampletype')
        if sampletype is None:
            initial['title'] = 'All'
        else:
            initial['title'] = [x[1] for x in SAMPLE_TYPES if x[0] == sampletype][0]
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
            qs = qs.filter(sample_type=sampletype)

        return qs


class SubSampleList(SingleTableMixin, ExportMixin, FilterView):
    """
    List of subsample by type
    """
    model = SubSample
    template_name = 'sample/sample-list.html'
    # paginate_by = 10
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
        return initial

    def get_queryset(self):
        sampletype = self.kwargs.get('sampletype')
        if sampletype is None:
            qs = SubSample.objects.all()
        else:
            print(sampletype)
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
        data = super(ShipmentCreate, self).get_initial()
        sample_id = self.kwargs.get('sampleid')
        self.sample = Sample.objects.get(pk=sample_id)
        data['subtitle'] = 'Create Shipment for Sample'
        data['sample'] = self.sample
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
        data['subtitle'] = 'Create Transform for Sample'
        data['sample'] = self.sample
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
        data['subtitle'] = 'Create Harvest record for Sample'
        data['sample'] = self.sample
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

    def get_initial(self, **kwargs):
        initial = super(SubSampleCreate, self).get_initial(**kwargs)
        if self.kwargs:
            sample_id = self.kwargs.get('sampleid')
            sample_type_key = self.kwargs.get('sampletype')
            sample_type = [item for item in SUBSAMPLE_TYPES if item[0] == sample_type_key]
            self.sample = Sample.objects.get(pk=sample_id)
            self.subtitle = 'Create %s subsample from Sample' % sample_type[0][1]
            initial['sample'] = self.sample
            initial['sample_type'] = sample_type[0]
            initial['sample_num'] = self.sample.get_next_subsample_num(sample_type[0][1])
        return initial

    def get_context_data(self, **kwargs):
        data = super(SubSampleCreate, self).get_context_data(**kwargs)
        data['subtitle'] = self.subtitle
        data['bookmark'] = 'SubSample'
        data['sample'] = self.sample
        if self.request.POST:
            data['location'] = LocationFormset(self.request.POST)
            data['qc'] = QCFormset(self.request.POST)
        else:
            data['location'] = LocationFormset()
            data['qc'] = QCFormset()
        return data

    def form_valid(self, form):
        try:
            context = self.get_context_data()
            location = context['location']
            qc = context['qc']
            # Save new location then add to storage_location
            with transaction.atomic():
                self.object = form.save()
            if qc.is_valid():
                qc.instance = self.object
                qc.save()
            if location.is_valid():
                subsample_location = location.save()
                self.object.location = subsample_location
            self.object.save()
            return super(SubSampleCreate, self).form_valid(form)
        except IntegrityError as e:
            msg = 'Database Error: Unable to create Sample - see Administrator: %s' % e
            form.add_error('id', msg)
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

    def get_context_data(self, **kwargs):
        data = super(SubSampleUpdate, self).get_context_data(**kwargs)
        data['subtitle'] = 'Edit SubSample'
        data['bookmark'] = self.get_object().get_sample_type_display()
        data['sample'] = self.get_object().sample
        if self.request.POST:
            data['location'] = LocationFormset(self.request.POST)
            data['qc'] = QCFormset(self.request.POST, instance=self.get_object())
        else:
            data['location'] = LocationFormset(instance=self.get_object().location)
            data['qc'] = QCFormset(instance=self.get_object())
        return data

    def form_valid(self, form):
        try:
            context = self.get_context_data()
            location = context['location']
            qc = context['qc']
            # Save new location then add to storage_location
            with transaction.atomic():
                self.object = form.save()
            if location.is_valid():
                subsample_location = location.save()
                self.object.location = subsample_location
            if qc.is_valid():
                qc.save()
            self.object.save()
            return super(SubSampleUpdate, self).form_valid(form)
        except IntegrityError as e:
            msg = 'Database Error: Unable to update SubSample - see Administrator: %s' % e
            form.add_error('Sample-update', msg)
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse('sample_detail', args=[self.object.sample.id])
