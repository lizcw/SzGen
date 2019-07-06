from django.shortcuts import render
from django.views.generic import FormView, CreateView, DetailView, UpdateView, RedirectView
from django.db import IntegrityError
from django.urls import reverse
from .models import Study
from .forms import StudyForm


def index(request):
    template = 'app/index.html'
    studies = Study.objects.all()
    context = {'studies': studies}
    return render(request, template, context)

######## STUDY ########
class StudyDetail(DetailView):
    """
    View details of a study
    """
    model = Study
    template_name = 'app/study.html'
    context_object_name = 'study'


class StudyCreate(CreateView):
    """
    Enter study data for new study
    """
    model = Study
    template_name = 'app/study-create.html'
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
    template_name = 'app/study-create.html'
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

