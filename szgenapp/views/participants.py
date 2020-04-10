import logging

from django.db import transaction
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView
from django_filters.views import FilterView
from django_tables2.export.views import ExportMixin
from django_tables2.views import SingleTableMixin
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


from szgenapp.filters.participants import *
from szgenapp.forms.participants import StudyParticipantForm, StudyParticipantRelatedForm
from szgenapp.tables.participants import *

logger = logging.getLogger(__name__)

######## STUDY PARTICIPANT ########
class StudyParticipantDetail(LoginRequiredMixin, DetailView):
    """
    View details of a study
    """
    model = StudyParticipant
    template_name = 'participant/participant.html'
    context_object_name = 'participant'


class StudyParticipantCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """
    Enter study data for new study
    """
    model = StudyParticipant
    template_name = 'participant/studyparticipant-create.html'
    form_class = StudyParticipantForm
    permission_required = 'szgenapp.add_studyparticipant'


    def get_success_url(self):
        return reverse('participant_detail', args=[self.object.id])

    def get_initial(self, *args, **kwargs):
        initial = super(StudyParticipantCreate, self).get_initial(**kwargs)
        initial['action'] = 'Create'
        return initial


class StudyParticipantUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """
    Enter study data for new study
    """
    model = StudyParticipant
    template_name = 'participant/studyparticipant-create.html'
    form_class = StudyParticipantForm
    permission_required = 'szgenapp.change_studyparticipant'


    def get_success_url(self):
        return reverse('participant_detail', args=[self.object.id])

    def get_initial(self, *args, **kwargs):
        initial = super(StudyParticipantUpdate, self).get_initial(**kwargs)
        initial['action'] = 'Update'
        return initial


class StudyParticipantList(SingleTableMixin, ExportMixin, FilterView):
    """
    List of Participants - filterable by study
    """
    model = StudyParticipant
    template_name = 'participant/studyparticipant-list.html'
    filterset_class = StudyParticipantFilter
    table_class = StudyParticipantTable

    def get_queryset(self):
        return StudyParticipant.objects.all().order_by('fullnumber')

class StudyParticipantDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """
    Delete a Participant and all studyparticipants, samples
    """
    model = StudyParticipant
    success_url = reverse_lazy("participants")
    template_name = 'participant/participant-confirm-delete.html'
    context_object_name = 'participant'
    permission_required = 'szgenapp.delete_studyparticipant'

class StudyParticipantAdd(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """
    Add a related participant
    """
    model = StudyParticipant
    template_name = 'participant/participant-related.html'
    context_object_name = 'participant'
    form_class = StudyParticipantRelatedForm
    permission_required = 'szgenapp.add_studyparticipant'

    def form_valid(self, form):
        """
        Participant lookup by fullnumber (not select - too slow)
        If the form is valid, redirect to the supplied URL.
        """
        related = form.cleaned_data['related_participant']
        if related is not None:
            with transaction.atomic():
                self.object = form.save(commit=False)
                try:
                    related_participant = StudyParticipant.objects.get(fullnumber__exact=related)
                    self.object.related_participant.add(related_participant)
                    self.object.save()
                    return HttpResponseRedirect(self.get_success_url())
                except StudyParticipant.DoesNotExist:
                    form.add_error('related_participant', 'Participant does not exist')
                    return super(StudyParticipantAdd, self).form_invalid(form)

        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        """Insert the form into the context dict."""
        if 'form' not in kwargs:
            form = self.get_form()
            form['related_participant'].initial = None
            kwargs['form'] = form
        return super().get_context_data(**kwargs)

    def get_success_url(self):
        return reverse('participant_detail', args=[self.object.id])

class StudyParticipantRemove(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """
    Remove a related participant
    """
    model = StudyParticipant
    template_name = 'participant/participant-confirm-remove.html'
    success_url = reverse_lazy("participants")
    permission_required = 'szgenapp.change_studyparticipant'

    def get_context_data(self, *args, **kwargs):
        data = super(StudyParticipantRemove, self).get_context_data(*args, **kwargs)
        pid = self.kwargs.get('participantid')
        related = StudyParticipant.objects.get(pk=pid)
        data['participant'] = related
        return data


    def delete(self, *args, **kwargs):
        pid = self.kwargs.get('participantid')
        related = StudyParticipant.objects.get(pk=pid)
        self.get_object().related_participant.remove(related)
        # Do not call super delete
        return HttpResponseRedirect(self.success_url)