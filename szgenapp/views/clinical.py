from django.views.generic import CreateView, DetailView, UpdateView, ListView
from django.db import IntegrityError, transaction
from django.urls import reverse

from szgenapp.models.clinical import Clinical, Demographic, Diagnosis, SymptomsBehaviour, SymptomsDelusion, SymptomsDepression, SymptomsGeneral, SymptomsHallucination, MedicalHistory
from szgenapp.forms.clinical import *
from szgenapp.models.participants import StudyParticipant

class ClinicalDetail(DetailView):
    model = Clinical
    template_name = 'clinical/clinical.html'
    context_object_name = 'clinical'

class ClinicalList(ListView):
    model = Clinical
    template_name = 'clinical/clinical-list.html'
    queryset = Clinical.objects.all()
    context_object_name = 'clinical'
    paginate_by = 10

class ClinicalCreate(CreateView):
    model = Clinical
    template_name = 'clinical/clinical-create.html'
    form_class = ClinicalForm

    def get_initial(self, *args, **kwargs):
        studyparticipant = None
        if (self.kwargs):
            pid = self.kwargs.get('participantid')
            studyparticipant = StudyParticipant.objects.get(pk=pid)
            # studyparticipant = participant.studyparticipants.first()  # TODO First of set by default
        initial = super(ClinicalCreate, self).get_initial(**kwargs)
        initial['action'] = 'Create'
        initial['participant'] = studyparticipant
        return initial

    def get_context_data(self, **kwargs):
        data = super(ClinicalCreate, self).get_context_data(**kwargs)
        data['title'] = 'Create Sample'
        if self.request.POST:
            data['demographic'] = DemographicFormset(self.request.POST)
            data['diagnosis'] = DiagnosisFormset(self.request.POST)
            data['medical'] = MedicalHistoryFormset(self.request.POST)
            data['symptoms_general'] = SymptomsGeneralFormset(self.request.POST)
            data['symptoms_delusion'] = SymptomsDelusionFormset(self.request.POST)
            data['symptoms_depression'] = SymptomsDepressionFormset(self.request.POST)
            data['symptoms_hallucination'] = SymptomsHallucinationFormset(self.request.POST)
            data['symptoms_behaviour'] = SymptomsBehaviourFormset(self.request.POST)
        else:
            data['demographic'] = DemographicFormset(instance=self.get_object())
            data['diagnosis'] = DiagnosisFormset(instance=self.get_object())
            data['medical'] = MedicalHistoryFormset(instance=self.get_object())
            data['symptoms_general'] = SymptomsGeneralFormset(instance=self.get_object())
            data['symptoms_delusion'] = SymptomsDelusionFormset(instance=self.get_object())
            data['symptoms_depression'] = SymptomsDepressionFormset(instance=self.get_object())
            data['symptoms_hallucination'] = SymptomsHallucinationFormset(instance=self.get_object())
            data['symptoms_behaviour'] = SymptomsBehaviourFormset(instance=self.get_object())
        return data
