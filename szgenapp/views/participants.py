from django.views.generic import CreateView, DetailView, UpdateView, ListView
from django.db import IntegrityError
from django.urls import reverse

from szgenapp.models.participants import Participant
from szgenapp.forms.participants import ParticipantForm

class ParticipantDetail(DetailView):
    """
    View details of a Participant
    """
    model = Participant
    template_name = 'participant/participant.html'
    context_object_name = 'Participant'


class ParticipantCreate(CreateView):
    """
    Enter Participant data for new Participant
    """
    model = Participant
    template_name = 'participant/participant-create.html'
    form_class = ParticipantForm

    def form_valid(self, form):
        try:
            return super(ParticipantCreate, self).form_valid(form)
        except IntegrityError as e:
            msg = 'Database Error: Unable to create Participant - see Administrator'
            form.add_error('Participant-create', msg)
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse('participant_detail', args=[self.object.id])

    def get_initial(self, *args, **kwargs):
        initial = super(ParticipantCreate, self).get_initial(**kwargs)
        initial['action'] = 'Create'
        return initial


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
