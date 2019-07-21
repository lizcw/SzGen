from django.views.generic import CreateView, DetailView, UpdateView, ListView
from django.db import IntegrityError, transaction
from django.urls import reverse

from szgenapp.models.samples import Sample, SubSample, HarvestSample, TransformSample, SUBSAMPLE_TYPES
from szgenapp.forms.samples import SampleForm, SubSampleForm, \
    LocationFormset, TransformSampleForm, HarvestSampleForm


class SampleDetail(DetailView):
    """
    View details of a blood sample
    """
    model = Sample
    template_name = 'sample/sample.html'
    context_object_name = 'sample'

    def get_context_data(self, **kwargs):
        data = super(SampleDetail, self).get_context_data(**kwargs)
        subsamples = data['sample'].subsample_set.all()
        data['lcytes'] = subsamples.filter(sample_type='LCTYE')
        data['lcl'] = subsamples.filter(sample_type='LCL')
        data['dna'] = subsamples.filter(sample_type='DNA')
        return data


class SampleCreate(CreateView):
    """
    Enter Sample data for new Sample
    """
    model = Sample
    template_name = 'sample/sample-create.html'
    form_class = SampleForm

    def get_context_data(self, **kwargs):
        data = super(SampleCreate, self).get_context_data(**kwargs)
        data['title'] = 'Create Sample'
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
                self.object = form.save(commit=False)
            if location.is_valid():
                storage_location = location.save()
                self.object.storage_location = storage_location
                self.object.save()
            return super(SampleCreate, self).form_valid(form)
        except IntegrityError as e:
            msg = 'Database Error: Unable to create Sample - see Administrator'
            form.add_error('sample-create', msg)
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
            msg = 'Database Error: Unable to update Sample - see Administrator'
            form.add_error('Sample-update', msg)
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse('sample_detail', args=[self.object.id])

    def get_initial(self, *args, **kwargs):
        initial = super(SampleUpdate, self).get_initial()
        initial['action'] = 'Edit'
        return initial


class SampleList(ListView):
    """
    List of Samples - filterable by study
    """
    model = Sample
    template_name = 'sample/sample-list.html'
    queryset = Sample.objects.all()
    context_object_name = 'samples'
    paginate_by = 10
    # ordering = ['']

    # def get_queryset(self):
    #     if self.request.GET.get('filter-by-study'):
    #         study = self.request.GET.get('filter-by-study')
    #         qs = self.queryset.filter(study=study)
    #     else:
    #         qs = self.queryset
    #     return qs


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
        data['title'] = 'Create Transform for Sample'
        data['sample'] = self.sample
        return data

    def get_success_url(self):
        return reverse('sample_detail', args=[self.sample.id])

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
        data['title'] = 'Create Harvest record for Sample'
        data['sample'] = self.sample
        return data

    def get_success_url(self):
        return reverse('sample_detail', args=[self.sample.id])

class SubSampleCreate(CreateView):
    """
    Add subsample of various types: Lymphocyte, LCL, DNA
    """
    model = SubSample
    template_name = 'sample/sample-create.html'
    form_class = SubSampleForm
    sample = Sample

    def get_initial(self):
        data = super(SubSampleCreate, self).get_initial()
        sample_id = self.kwargs.get('sampleid')
        sample_type_key = self.kwargs.get('sampletype')
        sample_type = [item for item in SUBSAMPLE_TYPES if item[0] == sample_type_key]
        self.sample = Sample.objects.get(pk=sample_id)
        data['title'] = 'Create % subsample from Sample' % sample_type[0][1]
        data['sample'] = self.sample
        data['sample_type'] = sample_type[0]
        return data

    def get_context_data(self, **kwargs):
        data = super(SubSampleCreate, self).get_context_data(**kwargs)
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
                self.object = form.save(commit=False)
            if location.is_valid():
                subsample_location = location.save()
                self.object.location = subsample_location
            self.object.save()
            return super(SubSampleCreate, self).form_valid(form)
        except IntegrityError as e:
            msg = 'Database Error: Unable to create Sample - see Administrator'
            form.add_error('id', msg)
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse('sample_detail', args=[self.sample.id])
