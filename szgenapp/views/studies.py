from django.shortcuts import render
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView
from django.db import IntegrityError
from django.db.models import Q
from django.urls import reverse, reverse_lazy
from django.core.paginator import Paginator

from szgenapp.models import Study, STATUS_CHOICES
from szgenapp.forms import StudyForm

#TODO Fix filtered list -> ListView
def index(request):
    """
    Home page - list of studies with filtering
    :param request:
    :return:
    """
    template = 'app/index.html'
    # filter on status
    status_options = list(STATUS_CHOICES)
    options = [('','--')]
    options += status_options

    if request.GET.get('filter-by-status'):
        status_filter = request.GET.get('filter-by-status')
        filter = [s[1] for s in STATUS_CHOICES if s[0] == status_filter]
        studies = Study.objects.filter(status=filter[0])
    else:
        studies = Study.objects.all().order_by('title')
    # Search query
    if request.GET.get('search'):
        searchtext = request.GET.get('search')
        studies = studies.filter(Q(title__icontains=searchtext) |
                                 Q(precursor__icontains=searchtext) |
                                 Q(description__icontains=searchtext))
    paginator = Paginator(studies, 4)
    page = request.GET.get('page')
    studies_page = paginator.get_page(page)
    context = {'studies': studies_page, 'statusOptions': options}
    return render(request, template, context)


######## STUDY ########
class StudyDetail(DetailView):
    """
    View details of a study
    """
    model = Study
    template_name = 'study/study.html'
    context_object_name = 'study'


class StudyCreate(CreateView):
    """
    Enter study data for new study
    """
    model = Study
    template_name = 'study/study-create.html'
    form_class = StudyForm

    def form_valid(self, form):
        try:
            return super(StudyCreate, self).form_valid(form)
        except IntegrityError as e:
            msg = 'Database Error: Unable to create Study - see Administrator: %s' % e
            form.add_error('title', msg)
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse('study_detail', args=[self.object.id])

    def get_initial(self, *args, **kwargs):
        initial = super(StudyCreate, self).get_initial(**kwargs)
        initial['action'] = 'Create'
        return initial



class StudyUpdate(UpdateView):
    """
    Enter study data for new study
    """
    model = Study
    template_name = 'study/study-create.html'
    form_class = StudyForm

    def form_valid(self, form):
        try:
            return super(StudyUpdate, self).form_valid(form)
        except IntegrityError as e:
            msg = 'Database Error: Unable to update Study - see Administrator: %s' % e
            form.add_error('title', msg)
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse('study_detail', args=[self.object.id])

    def get_initial(self, *args, **kwargs):
        initial = super(StudyUpdate, self).get_initial(**kwargs)
        initial['action'] = 'Create'
        return initial


class StudyDelete(DeleteView):
    """
    Delete a Study and all participants
    """
    model = Study
    success_url = reverse_lazy("index")
    template_name = 'study/study-confirm-delete.html'
