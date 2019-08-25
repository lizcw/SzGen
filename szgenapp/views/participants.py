from django.views.generic import CreateView, DetailView, UpdateView, ListView
from django.db import IntegrityError, transaction
from django.urls import reverse
from django_filters.views import FilterView
from django_tables2.export.views import ExportMixin
from django_tables2.views import SingleTableMixin

from szgenapp.models.participants import Participant, StudyParticipant
from szgenapp.models.samples import SUBSAMPLE_TYPES
from szgenapp.forms.participants import ParticipantForm, StudyParticipantForm, StudyParticipantFormset
from szgenapp.tables.participants import *
from szgenapp.filters.participants import *


class ParticipantDetail(DetailView):
    """
    View details of a Participant
    """
    model = Participant
    template_name = 'participant/participant.html'
    context_object_name = 'participant'

    def get_context_data(self, **kwargs):
        context = super(ParticipantDetail, self).get_context_data(**kwargs)
        context['subsampletypes'] = SUBSAMPLE_TYPES
        return context


class ParticipantCreate(CreateView):
    """
    Enter Participant data for new Participant
    """
    model = Participant
    template_name = 'participant/participant-create.html'
    form_class = ParticipantForm

    def get_context_data(self, **kwargs):
        data = super(ParticipantCreate, self).get_context_data(**kwargs)
        data['action'] = 'Create'
        if self.request.POST:
            data['studyparticipant'] = StudyParticipantFormset(self.request.POST)
        else:
            data['studyparticipant'] = StudyParticipantFormset()
        return data

    def form_valid(self, form):
        try:
            context = self.get_context_data()
            subform = context['studyparticipant']
            with transaction.atomic():
                self.object = form.save()

            if subform.is_valid():
                subform.instance = self.object
                subform.save()
            return super(ParticipantCreate, self).form_valid(form)
        except IntegrityError as e:
            msg = 'Database Error: Unable to create Participant - see Administrator'
            form.add_error('Participant-create', msg)
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse('participant_detail', args=[self.object.id])



class ParticipantUpdate(UpdateView):
    """
    Enter Participant data for new Participant
    """
    model = Participant
    template_name = 'participant/participant-create.html'
    form_class = ParticipantForm

    def form_valid(self, form):
        try:
            return super(ParticipantUpdate, self).form_valid(form)
        except IntegrityError as e:
            msg = 'Database Error: Unable to update Participant - see Administrator'
            form.add_error('Participant-update', msg)
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse('participant_detail', args=[self.object.id])

    def get_initial(self, *args, **kwargs):
        initial = super(ParticipantUpdate, self).get_initial(**kwargs)
        initial['action'] = 'Edit'
        return initial


class ParticipantList(ListView):
    """
    List of Participants - filterable by study
    """
    model = Participant
    template_name = 'participant/participant-list.html'
    queryset = Participant.objects.all()
    context_object_name = 'participants'
    paginate_by = 10
    # ordering = ['']

    def get_queryset(self):
        if self.request.GET.get('filter-by-study'):
            study = self.request.GET.get('filter-by-study')
            qs = self.queryset.filter(study=study)
        else:
            qs = self.queryset
        return qs


######## STUDY PARTICIPANT ########
class StudyParticipantDetail(DetailView):
    """
    View details of a study
    """
    model = StudyParticipant
    template_name = 'participant/participant.html'
    context_object_name = 'studyparticipant'


class StudyParticipantCreate(CreateView):
    """
    Enter study data for new study
    """
    model = StudyParticipant
    template_name = 'participant/studyparticipant-create.html'
    form_class = StudyParticipantForm

    def form_valid(self, form):
        try:
            with transaction.atomic():
                self.object = form.save(commit=False)
            self.object.participant = form.initial['participant']
            self.object.save()
            return super(StudyParticipantCreate, self).form_valid(form)
        except IntegrityError as e:
            msg = 'Database Error: Unable to create StudyParticipant - see Administrator'
            form.add_error('error', msg)
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse('participant_detail', args=[self.object.participant.id])

    def get_initial(self, *args, **kwargs):
        pid = self.kwargs.get('participantid')
        initial = super(StudyParticipantCreate, self).get_initial(**kwargs)
        initial['action'] = 'Create'
        initial['participant'] = Participant.objects.get(pk=pid)
        return initial



class StudyParticipantUpdate(UpdateView):
    """
    Enter study data for new study
    """
    model = StudyParticipant
    template_name = 'participant/studyparticipant-create.html'
    form_class = StudyParticipantForm

    def form_valid(self, form):
        try:
            return super(StudyParticipantUpdate, self).form_valid(form)
        except IntegrityError as e:
            msg = 'Database Error: Unable to update Study - see Administrator'
            form.add_error('studyparticipant-update', msg)
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse('studyparticipant_detail', args=[self.object.id])

    def get_initial(self, *args, **kwargs):
        initial = super(StudyParticipantUpdate, self).get_initial(**kwargs)
        initial['action'] = 'Create'
        return initial


class StudyParticipantList(SingleTableMixin, ExportMixin, FilterView):
    """
    List of Participants - filterable by study
    """
    model = StudyParticipant
    template_name = 'participant/studyparticipant-list.html'
    filterset_class = StudyParticipantFilter
    table_class = StudyParticipantTable

    # def get_queryset(self, **kwargs):
    #     study = self.kwargs.get('study')
    #     if study is None:
    #         qs = StudyParticipant.objects.all()
    #     else:
    #         qs = StudyParticipant.objects.filter(study__id=study)
    #
    #     return qs
