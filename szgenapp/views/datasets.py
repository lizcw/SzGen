import logging

from django.db import IntegrityError, transaction
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView
from django_filters.views import FilterView
from django_tables2.export.views import ExportMixin
from django_tables2.views import SingleTableMixin
from django_tables2 import RequestConfig

from szgenapp.filters.dataset import DatasetFilter, DatasetFileFilter, DatasetParticipantFilter
from szgenapp.forms.datasets import DatasetForm, DatasetFileFormset, DatasetRowForm, DatasetFileForm
from szgenapp.models.datasets import Dataset, DatasetRow, DatasetFile
from szgenapp.models.participants import StudyParticipant
from szgenapp.models.studies import Study
from szgenapp.tables.dataset import DatasetTable, DatasetFileTable, DatasetParticipantTable

logger = logging.getLogger(__name__)


class DatasetDetail(DetailView):
    """
    View details of a Dataset
    """
    model = Dataset
    template_name = 'dataset/dataset.html'
    context_object_name = 'dataset'

    def get_context_data(self, **kwargs):
        data = super(DatasetDetail, self).get_context_data(**kwargs)
        qs = DatasetRow.objects.filter(dataset=self.object).order_by('participant__fullnumber')
        table = DatasetParticipantTable(qs)
        RequestConfig(self.request, paginate={"per_page": 10}).configure(table)
        data['participant_table'] = table
        return data


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
            msg = 'Database Error: Unable to create Dataset - see Administrator: %s' % e
            form.add_error(None, msg)
            logger.error(msg)
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse('dataset_detail', args=[self.object.dataset.id])


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
            msg = 'Database Error: Unable to update Dataset - see Administrator: %s' % e
            form.add_error(None, msg)
            logger.error(msg)
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse('dataset_detail', args=[self.object.dataset.id])


class DatasetDelete(DeleteView):
    """
    Delete a Dataset and all dataset participants, files
    """
    model = Dataset
    success_url = reverse_lazy("datasets")
    template_name = 'dataset/dataset-confirm-delete.html'


class DatasetParticipantUpdate(UpdateView):
    """
    Enter Participant data for a Dataset
    """
    model = DatasetRow
    template_name = 'dataset/dataset-create.html'
    form_class = DatasetRowForm

    def get_context_data(self, **kwargs):
        data = super(DatasetParticipantUpdate, self).get_context_data(**kwargs)
        data['action'] = 'Edit'
        data['subtitle'] = 'Participant'
        return data

    def get_success_url(self):
        return reverse('dataset_detail', args=[self.object.dataset.id])


class DatasetList(SingleTableMixin, ExportMixin, FilterView):
    """
    List of Datasets - filterable by group
    """
    model = Dataset
    template_name = 'dataset/dataset-list.html'
    filterset_class = DatasetFilter
    table_class = DatasetTable

    def get_context_data(self, *args, **kwargs):
        context = super(DatasetList, self).get_context_data(*args, **kwargs)
        context['reset_url'] = 'datasets'
        context['title'] = 'Summary'
        studyid = self.kwargs.get('study')
        if studyid is not None:
            study = Study.objects.get(pk=studyid)
            context['title'] += ' for ' + study.title
        return context

    def get_queryset(self, **kwargs):
        study = self.kwargs.get('study')
        if study is None:
            qs = Dataset.objects.all()
        else:
            qs = Dataset.objects.filter(dataset_participants__participant__study_id__exact=study)

        return qs


class DatasetFileList(SingleTableMixin, ExportMixin, FilterView):
    """
    List of Dataset Files with filters
    """
    model = DatasetFile
    template_name = 'dataset/dataset-list.html'
    filterset_class = DatasetFileFilter
    table_class = DatasetFileTable

    def get_context_data(self, *args, **kwargs):
        context = super(DatasetFileList, self).get_context_data(*args, **kwargs)
        context['reset_url'] = 'dataset_files'
        context['title'] = 'Files'
        return context


class DatasetParticipantList(SingleTableMixin, ExportMixin, FilterView):
    """
    List of Dataset Participants with filters
    """
    model = DatasetRow
    template_name = 'dataset/dataset-list.html'
    filterset_class = DatasetParticipantFilter
    table_class = DatasetParticipantTable

    def get_context_data(self, *args, **kwargs):
        context = super(DatasetParticipantList, self).get_context_data(*args, **kwargs)
        context['reset_url'] = 'dataset_participants'
        context['title'] = 'Participants'
        return context


class DatasetRowCreate(CreateView):
    """
    Enter Dataset data for Participant
    """
    model = DatasetRow
    template_name = 'dataset/dataset-create.html'
    form_class = DatasetRowForm

    def get_initial(self, *args, **kwargs):
        initial = super(DatasetRowCreate, self).get_initial(**kwargs)
        initial['action'] = 'Create'
        if self.kwargs.get('datasetid'):
            did = self.kwargs.get('datasetid')
            initial['dataset'] = Dataset.objects.get(pk=did)
        if self.kwargs.get('participantid'):
            pid = self.kwargs.get('participantid')
            initial['participant'] = StudyParticipant.objects.get(pk=pid)
        return initial

    def get_context_data(self, **kwargs):
        data = super(DatasetRowCreate, self).get_context_data(**kwargs)
        data['action'] = 'Create'
        data['subtitle'] = 'Participant'
        return data

    def get_success_url(self):
        return reverse('dataset_detail', args=[self.object.dataset.id])


class DatasetFileCreate(CreateView):
    """
    Create a dataset file for a dataset
    """
    model = DatasetFile
    template_name = 'dataset/dataset-create.html'
    form_class = DatasetFileForm

    def get_initial(self, *args, **kwargs):
        initial = super(DatasetFileCreate, self).get_initial(**kwargs)
        initial['action'] = 'Create'
        if self.kwargs.get('datasetid'):
            did = self.kwargs.get('datasetid')
            initial['dataset'] = Dataset.objects.get(pk=did)
        return initial

    def get_success_url(self):
        return reverse('dataset_detail', args=[self.object.dataset.id])


class DatasetFileUpdate(UpdateView):
    """
    Update a dataset file for a dataset
    """
    model = DatasetFile
    template_name = 'dataset/dataset-create.html'
    form_class = DatasetFileForm

    def get_initial(self, *args, **kwargs):
        initial = super(self.__class__, self).get_initial(**kwargs)
        initial['action'] = 'Edit'
        return initial

    def get_success_url(self):
        return reverse('dataset_detail', args=[self.object.dataset.id])
