import logging

from django.db import IntegrityError, transaction
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView
from django_filters.views import FilterView
from django_tables2.export.views import ExportMixin
from django_tables2.views import SingleTableMixin
from django_tables2 import RequestConfig
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


from szgenapp.filters.dataset import DatasetFilter, DatasetFileFilter, DatasetParticipantFilter
from szgenapp.forms.datasets import DatasetForm, DatasetFileFormset, DatasetRowForm, DatasetFileForm
from szgenapp.models.datasets import Dataset, DatasetRow, DatasetFile
from szgenapp.models.participants import StudyParticipant
from szgenapp.models.studies import Study
from szgenapp.tables.dataset import DatasetTable, DatasetFileTable, DatasetParticipantTable

logger = logging.getLogger(__name__)


class DatasetDetail(LoginRequiredMixin, DetailView):
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


class DatasetCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """
    Enter Dataset data for new Dataset
    """
    model = Dataset
    template_name = 'dataset/dataset-create.html'
    form_class = DatasetForm
    permission_required = 'szgenapp.add_dataset'

    def get_success_url(self):
        return reverse('dataset_detail', args=[self.object.id])


class DatasetUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """
    Enter Dataset data for new Dataset
    """
    model = Dataset
    template_name = 'dataset/dataset-create.html'
    form_class = DatasetForm
    permission_required = 'szgenapp.change_dataset'

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
        return reverse('dataset_detail', args=[self.object.id])


class DatasetDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """
    Delete a Dataset and all dataset participants, files
    """
    model = Dataset
    success_url = reverse_lazy("datasets")
    template_name = 'dataset/dataset-confirm-delete.html'
    permission_required = 'szgenapp.delete_dataset'


class DatasetParticipantUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """
    Enter Participant data for a Dataset
    """
    model = DatasetRow
    template_name = 'dataset/dataset-create.html'
    form_class = DatasetRowForm
    permission_required = 'szgenapp.change_datasetrow'

    def get_initial(self):
        data = super(DatasetParticipantUpdate, self).get_initial()
        data['participant_fullnumber'] = self.get_object().participant.fullnumber
        return data

    def get_context_data(self, **kwargs):
        data = super(DatasetParticipantUpdate, self).get_context_data(**kwargs)
        data['action'] = 'Edit'
        data['subtitle'] = 'Participant'
        return data

    def form_valid(self, form):
        """
        Participant lookup by fullnumber (not select - too slow)
        If the form is valid, redirect to the supplied URL.
        """
        participant_new = form.cleaned_data['participant_fullnumber']
        if participant_new is not None:
            with transaction.atomic():
                self.object = form.save(commit=False)
                try:
                    if self.object.participant is None or self.object.participant.fullnumber != participant_new:
                        new_participant = StudyParticipant.objects.get(fullnumber__exact=participant_new)
                        self.object.participant = new_participant
                    self.object.save()
                    return HttpResponseRedirect(self.get_success_url())
                except StudyParticipant.DoesNotExist:
                    form.add_error('participant_fullnumber', 'Participant does not exist')
                    return super(DatasetParticipantUpdate, self).form_invalid(form)

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


class DatasetRowCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """
    Enter Dataset data for Participant
    """
    model = DatasetRow
    template_name = 'dataset/dataset-create.html'
    form_class = DatasetRowForm
    permission_required = 'szgenapp.add_datasetrow'

    def get_initial(self, *args, **kwargs):
        initial = super(DatasetRowCreate, self).get_initial(**kwargs)
        initial['action'] = 'Create'
        if self.kwargs.get('datasetid'):
            did = self.kwargs.get('datasetid')
            initial['dataset'] = Dataset.objects.get(pk=did)
        if self.kwargs.get('participantid'):
            pid = self.kwargs.get('participantid')
            participant = StudyParticipant.objects.get(pk=pid)
            initial['participant_fullnumber'] = participant.fullnumber
        return initial

    def form_valid(self, form):
        """
        Participant lookup by fullnumber (not select - too slow)
        If the form is valid, redirect to the supplied URL.
        """
        participant_new = form.cleaned_data['participant_fullnumber']
        if participant_new is not None:
            with transaction.atomic():
                self.object = form.save(commit=False)
                try:
                    new_participant = StudyParticipant.objects.get(fullnumber__exact=participant_new)
                    self.object.participant = new_participant
                    self.object.save()
                    return HttpResponseRedirect(self.get_success_url())
                except StudyParticipant.DoesNotExist:
                    form.add_error('participant_fullnumber', 'Participant does not exist')
                    return super(DatasetRowCreate, self).form_invalid(form)

    def get_context_data(self, **kwargs):
        data = super(DatasetRowCreate, self).get_context_data(**kwargs)
        data['action'] = 'Create'
        data['subtitle'] = 'Participant'
        return data

    def get_success_url(self):
        return reverse('dataset_detail', args=[self.object.dataset.id])


class DatasetFileCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """
    Create a dataset file for a dataset
    """
    model = DatasetFile
    template_name = 'dataset/dataset-create.html'
    form_class = DatasetFileForm
    permission_required = 'szgenapp.add_datasetfile'

    def get_initial(self, *args, **kwargs):
        initial = super(DatasetFileCreate, self).get_initial(**kwargs)
        initial['action'] = 'Create'
        if self.kwargs.get('datasetid'):
            did = self.kwargs.get('datasetid')
            initial['dataset'] = Dataset.objects.get(pk=did)
        return initial

    def get_success_url(self):
        return reverse('dataset_detail', args=[self.object.dataset.id])


class DatasetFileUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """
    Update a dataset file for a dataset
    """
    model = DatasetFile
    template_name = 'dataset/dataset-create.html'
    form_class = DatasetFileForm
    permission_required = 'szgenapp.change_datasetfile'

    def get_initial(self, *args, **kwargs):
        initial = super(self.__class__, self).get_initial(**kwargs)
        initial['action'] = 'Edit'
        return initial

    def get_success_url(self):
        return reverse('dataset_detail', args=[self.object.dataset.id])
