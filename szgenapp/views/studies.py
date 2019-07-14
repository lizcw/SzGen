from django.shortcuts import render
from django.views.generic import FormView, CreateView, DetailView, UpdateView, RedirectView
from django.db import IntegrityError
from django.db.models import Q
from django.urls import reverse
from django.core.paginator import Paginator

from szgenapp.models import Study, STATUS_CHOICES
from szgenapp.forms import StudyForm


def index(request):
    """
    Home page - list of studies with filtering
    :param request:
    :return:
    """
    template = 'app/index.html'
    # filter on status
    status_options = STATUS_CHOICES
    if request.GET.get('filter-by-status'):
        status_filter = request.GET.get('filter-by-status')
        # Currently only allows single selection
        if isinstance(status_filter, list):
            studies = Study.objects.filter(status__in=status_filter)
        else:
            studies = Study.objects.filter(status=status_filter)
    else:
        studies = Study.objects.all()
    # Search query
    if request.GET.get('search'):
        searchtext = request.GET.get('search')
        studies = studies.filter(Q(title__icontains=searchtext) |
                                 Q(precursor__icontains=searchtext) |
                                 Q(description__icontains=searchtext))
    paginator = Paginator(studies, 4)
    page = request.GET.get('page')
    studies_page = paginator.get_page(page)
    context = {'studies': studies_page, 'statusOptions': status_options}
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
            msg = 'Database Error: Unable to create Study - see Administrator'
            form.add_error('study-create', msg)
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse('study_detail', args=[self.object.id])


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
            msg = 'Database Error: Unable to update Study - see Administrator'
            form.add_error('study-update', msg)
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse('study_detail', args=[self.object.id])

