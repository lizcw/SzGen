from django.views.generic import CreateView, DetailView, UpdateView, ListView
from django.db import IntegrityError, transaction
from django.urls import reverse

from szgenapp.models.datasets import Dataset, DatasetRow, DatasetFile
from szgenapp.models.participants import Participant
from szgenapp.forms.datasets import DatasetForm, DatasetFileFormset, DatasetParticipantFormset, DatasetRowForm


class DatasetDetail(DetailView):
    """
    View details of a Dataset
    """
    model = Dataset
    template_name = 'dataset/dataset.html'
    context_object_name = 'dataset'


class DatasetCreate(CreateView):
    """
    Enter Dataset data for new Dataset
    """
    model = Dataset
    template_name = 'dataset/dataset-create.html'
    form_class = DatasetForm

    def get_context_data(self, **kwargs):
        data = super(DatasetCreate, self).get_context_data(**kwargs)
        data['action'] = 'Create'
        if self.request.POST:
            data['datasetfiles'] = DatasetFileFormset(self.request.POST)
        else:
            data['datasetfiles'] = DatasetFileFormset()
        return data

    def form_valid(self, form):
        try:
            context = self.get_context_data()
            datasetfiles = context['datasetfiles']
            with transaction.atomic():
                self.object = form.save()

            if datasetfiles.is_valid():
                datasetfiles.instance = self.object
                datasetfiles.save()
            return super(DatasetCreate, self).form_valid(form)
        except IntegrityError as e:
            msg = 'Database Error: Unable to create Dataset - see Administrator'
            form.add_error('dataset-create', msg)
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse('datasets')




class DatasetUpdate(UpdateView):
    """
    Enter Dataset data for new Dataset
    """
    model = Dataset
    template_name = 'dataset/dataset-create.html'
    form_class = DatasetForm

    def get_context_data(self, **kwargs):
        data = super(DatasetUpdate, self).get_context_data(**kwargs)
        data['action'] = 'Edit'
        data['datasetname'] = 'Dataset Files'
        if self.request.POST:
            data['datasetfiles'] = DatasetFileFormset(self.request.POST, instance=self.get_object())
        else:
            data['datasetfiles'] = DatasetFileFormset(instance=self.get_object())
            data['datasetfiles'].extra = 1
        return data

    def form_valid(self, form):
        try:
            context = self.get_context_data()
            datasetfiles = context['datasetfiles']
            with transaction.atomic():
                self.object = form.save()
                if datasetfiles.is_valid():
                    datasetfiles.save()

            return super(DatasetUpdate, self).form_valid(form)

        except IntegrityError as e:
            msg = 'Database Error: Unable to update Dataset - see Administrator'
            form.add_error('Dataset-update', msg)
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse('datasets')


class DatasetParticipantUpdate(UpdateView):
    """
    Enter Participant data for a Dataset
    """
    model = Dataset
    template_name = 'dataset/dataset-create.html'
    form_class = DatasetForm

    def get_context_data(self, **kwargs):
        data = super(DatasetParticipantUpdate, self).get_context_data(**kwargs)
        data['action'] = 'Edit'
        data['datasetname'] = 'Participants'
        if self.request.POST:
            data['datasetfiles'] = DatasetParticipantFormset(self.request.POST, instance=self.get_object())
        else:
            data['datasetfiles'] = DatasetParticipantFormset(instance=self.get_object())
            data['datasetfiles'].extra = 1
        return data

    def form_valid(self, form):
        try:
            context = self.get_context_data()
            datasetfiles = context['datasetfiles']
            with transaction.atomic():
                self.object = form.save()
                if datasetfiles.is_valid():
                    datasetfiles.save()

            return super(DatasetParticipantUpdate, self).form_valid(form)

        except IntegrityError as e:
            msg = 'Database Error: Unable to update Dataset - see Administrator'
            form.add_error('Dataset-update', msg)
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse('datasets')


class DatasetList(ListView):
    """
    List of Datasets - filterable by group
    """
    model = Dataset
    template_name = 'dataset/dataset-list.html'
    queryset = Dataset.objects.all()
    context_object_name = 'datasets'
    paginate_by = 10
    # ordering = ['']

    def get_queryset(self):
        if self.request.GET.get('filter-by-group'):
            group = self.request.GET.get('filter-by-group')
            qs = self.queryset.filter(dataset__group=group)
        else:
            qs = self.queryset
        return qs


class DatasetRowCreate(CreateView):
    """
    Enter Dataset data for Participant
    """
    model = DatasetRow
    template_name = 'dataset/dataset-create.html'
    form_class = DatasetRowForm

    def get_initial(self, *args, **kwargs):
        pid = self.kwargs.get('participantid')
        initial = super(DatasetRowCreate, self).get_initial(**kwargs)
        initial['action'] = 'Create'
        initial['participant'] = Participant.objects.get(pk=pid)
        return initial

    def form_valid(self, form):
        try:
            with transaction.atomic():
                self.object = form.save(commit=False)
            self.object.participant = form.initial['participant']
            self.object.save()
            return super(DatasetRowCreate, self).form_valid(form)
        except IntegrityError as e:
            msg = 'Database Error: Unable to create Dataset - see Administrator'
            form.add_error('error', msg)
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse('datasets')