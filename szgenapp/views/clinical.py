from django.views.generic import CreateView, DetailView, ListView, UpdateView
from django.urls import reverse
from szgenapp.forms.clinical import *
from szgenapp.models.participants import StudyParticipant
from szgenapp.models.clinical import *


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
        initial = super(ClinicalCreate, self).get_initial(**kwargs)
        initial['action'] = 'Create'
        initial['participant'] = studyparticipant
        return initial

    def get_context_data(self, **kwargs):
        data = super(ClinicalCreate, self).get_context_data(**kwargs)
        data['title'] = 'Create Clinical Record'
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
            data['demographic'] = DemographicFormset()
            data['diagnosis'] = DiagnosisFormset()
            data['medical'] = MedicalHistoryFormset()
            data['symptoms_general'] = SymptomsGeneralFormset()
            data['symptoms_delusion'] = SymptomsDelusionFormset()
            data['symptoms_depression'] = SymptomsDepressionFormset()
            data['symptoms_hallucination'] = SymptomsHallucinationFormset()
            data['symptoms_behaviour'] = SymptomsBehaviourFormset()
        data['tablist'] = [(key, key.replace('_', ': ').upper()) for key in data.keys() if key != 'form' and
                           key != 'view' and key != 'title']
        return data

    def get_success_url(self):
        return reverse('clinical_detail', args=[self.object.participant.id])


class ClinicalUpdate(UpdateView):
    model = Clinical
    template_name = 'clinical/clinical-create.html'
    form_class = ClinicalForm

    def get_initial(self, *args, **kwargs):
        initial = super(ClinicalUpdate, self).get_initial(**kwargs)
        initial['action'] = 'Create'
        return initial

    def get_context_data(self, **kwargs):
        data = super(ClinicalUpdate, self).get_context_data(**kwargs)
        data['title'] = 'Update Clinical Record'
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
        data['tablist'] = [(key, key.replace('_', ': ').upper()) for key in data.keys() if key != 'form' and
                           key != 'view' and key != 'title' and key != 'object' and key != 'clinical']
        return data

    def get_success_url(self):
        return reverse('clinical_detail', args=[self.object.participant.id])


class ClinicalDemographicCreate(CreateView):
    model = Demographic
    template_name = 'clinical/clinical-sub-create.html'
    form_class = DemographicForm

    def get_initial(self, *args, **kwargs):
        studyparticipant = None
        if (self.kwargs):
            pid = self.kwargs.get('clinicalid')
            studyparticipant = Clinical.objects.get(pk=pid)
        initial = super(ClinicalDemographicCreate, self).get_initial(**kwargs)
        initial['title'] = 'Create Clinical Demographic Record'
        initial['participant'] = studyparticipant
        return initial

    def get_success_url(self):
        return reverse('clinical_detail', args=[self.object.participant.id])


class ClinicalDemographicUpdate(UpdateView):
    model = Demographic
    template_name = 'clinical/clinical-sub-create.html'
    form_class = DemographicForm

    def get_initial(self, *args, **kwargs):
        initial = super(ClinicalDemographicUpdate, self).get_initial(**kwargs)
        initial['title'] = 'Update Clinical Demographic Record'
        return initial

    def get_success_url(self):
        return reverse('clinical_detail', args=[self.object.participant.id])


class ClinicalDiagnosisCreate(CreateView):
    model = Diagnosis
    template_name = 'clinical/clinical-sub-create.html'
    form_class = DiagnosisForm

    def get_initial(self, *args, **kwargs):
        studyparticipant = None
        if (self.kwargs):
            pid = self.kwargs.get('clinicalid')
            studyparticipant = Clinical.objects.get(pk=pid)
        initial = super(ClinicalDiagnosisCreate, self).get_initial(**kwargs)
        initial['title'] = 'Create Clinical Diagnosis Record'
        initial['participant'] = studyparticipant
        return initial

    def get_success_url(self):
        return reverse('clinical_detail', args=[self.object.participant.id])


class ClinicalDiagnosisUpdate(UpdateView):
    model = Diagnosis
    template_name = 'clinical/clinical-sub-create.html'
    form_class = DiagnosisForm

    def get_initial(self, *args, **kwargs):
        initial = super(ClinicalDiagnosisUpdate, self).get_initial(**kwargs)
        initial['title'] = 'Update Clinical Diagnosis Record'
        return initial

    def get_success_url(self):
        return reverse('clinical_detail', args=[self.object.participant.id])


class ClinicalMedicalCreate(CreateView):
    model = MedicalHistory
    template_name = 'clinical/clinical-sub-create.html'
    form_class = MedicalHistoryForm

    def get_initial(self, *args, **kwargs):
        studyparticipant = None
        if (self.kwargs):
            pid = self.kwargs.get('clinicalid')
            studyparticipant = Clinical.objects.get(pk=pid)
        initial = super(ClinicalMedicalCreate, self).get_initial(**kwargs)
        initial['title'] = 'Create Clinical Medical Record'
        initial['participant'] = studyparticipant
        return initial

    def get_success_url(self):
        return reverse('clinical_detail', args=[self.object.participant.id])


class ClinicalMedicalUpdate(UpdateView):
    model = MedicalHistory
    template_name = 'clinical/clinical-sub-create.html'
    form_class = MedicalHistoryForm

    def get_initial(self, *args, **kwargs):
        initial = super(ClinicalMedicalUpdate, self).get_initial(**kwargs)
        initial['title'] = 'Update Clinical Medical Record'
        return initial

    def get_success_url(self):
        return reverse('clinical_detail', args=[self.object.participant.id])


class ClinicalSymptomsGeneralCreate(CreateView):
    model = SymptomsGeneral
    template_name = 'clinical/clinical-sub-create.html'
    form_class = SymptomsGeneralForm

    def get_initial(self, *args, **kwargs):
        studyparticipant = None
        if (self.kwargs):
            pid = self.kwargs.get('clinicalid')
            studyparticipant = Clinical.objects.get(pk=pid)
        initial = super(ClinicalSymptomsGeneralCreate, self).get_initial(**kwargs)
        initial['title'] = 'Create Clinical General Symptoms Record'
        initial['participant'] = studyparticipant
        return initial

    def get_success_url(self):
        return reverse('clinical_detail', args=[self.object.participant.id])


class ClinicalSymptomsGeneralUpdate(UpdateView):
    model = SymptomsGeneral
    template_name = 'clinical/clinical-sub-create.html'
    form_class = SymptomsGeneralForm

    def get_initial(self, *args, **kwargs):
        initial = super(ClinicalSymptomsGeneralUpdate, self).get_initial(**kwargs)
        initial['title'] = 'Update Clinical General Symptoms Record'
        return initial

    def get_success_url(self):
        return reverse('clinical_detail', args=[self.object.participant.id])


class ClinicalSymptomsDelusionCreate(CreateView):
    model = SymptomsDelusion
    template_name = 'clinical/clinical-sub-create.html'
    form_class = SymptomsDelusionForm

    def get_initial(self, *args, **kwargs):
        studyparticipant = None
        if (self.kwargs):
            pid = self.kwargs.get('clinicalid')
            studyparticipant = Clinical.objects.get(pk=pid)
        initial = super(ClinicalSymptomsDelusionCreate, self).get_initial(**kwargs)
        initial['title'] = 'Create Clinical Delusion Symptoms Record'
        initial['participant'] = studyparticipant
        return initial

    def get_success_url(self):
        return reverse('clinical_detail', args=[self.object.participant.id])


class ClinicalSymptomsDelusionUpdate(UpdateView):
    model = Demographic
    template_name = 'clinical/clinical-sub-create.html'
    form_class = DemographicForm

    def get_initial(self, *args, **kwargs):
        initial = super(ClinicalSymptomsDelusionUpdate, self).get_initial(**kwargs)
        initial['title'] = 'Update Clinical Delusion Symptoms Record'
        return initial

    def get_success_url(self):
        return reverse('clinical_detail', args=[self.object.participant.id])


class ClinicalSymptomsHallucinationCreate(CreateView):
    model = SymptomsHallucination
    template_name = 'clinical/clinical-sub-create.html'
    form_class = SymptomsHallucinationForm

    def get_initial(self, *args, **kwargs):
        studyparticipant = None
        if (self.kwargs):
            pid = self.kwargs.get('clinicalid')
            studyparticipant = Clinical.objects.get(pk=pid)
        initial = super(ClinicalSymptomsHallucinationCreate, self).get_initial(**kwargs)
        initial['title'] = 'Create Clinical Hallucination Symptoms Record'
        initial['participant'] = studyparticipant
        return initial

    def get_success_url(self):
        return reverse('clinical_detail', args=[self.object.participant.id])


class ClinicalSymptomsHallucinationUpdate(UpdateView):
    model = SymptomsHallucination
    template_name = 'clinical/clinical-sub-create.html'
    form_class = SymptomsHallucinationForm

    def get_initial(self, *args, **kwargs):
        initial = super(ClinicalSymptomsHallucinationUpdate, self).get_initial(**kwargs)
        initial['title'] = 'Update Clinical Hallucination Symptoms Record'
        return initial

    def get_success_url(self):
        return reverse('clinical_detail', args=[self.object.participant.id])


class ClinicalSymptomsBehaviourCreate(CreateView):
    model = SymptomsBehaviour
    template_name = 'clinical/clinical-sub-create.html'
    form_class = SymptomsBehaviourForm

    def get_initial(self, *args, **kwargs):
        studyparticipant = None
        if (self.kwargs):
            pid = self.kwargs.get('clinicalid')
            studyparticipant = Clinical.objects.get(pk=pid)
        initial = super(ClinicalSymptomsBehaviourCreate, self).get_initial(**kwargs)
        initial['title'] = 'Create Clinical Behaviour Symptoms Record'
        initial['participant'] = studyparticipant
        return initial

    def get_success_url(self):
        return reverse('clinical_detail', args=[self.object.participant.id])


class ClinicalSymptomsBehaviourUpdate(UpdateView):
    model = SymptomsBehaviour
    template_name = 'clinical/clinical-sub-create.html'
    form_class = SymptomsBehaviourForm

    def get_initial(self, *args, **kwargs):
        initial = super(ClinicalSymptomsBehaviourUpdate, self).get_initial(**kwargs)
        initial['title'] = 'Update Clinical Behaviour Symptoms Record'
        # initial['participant'] = studyparticipant
        return initial

    def get_success_url(self):
        return reverse('clinical_detail', args=[self.object.participant.id])


class ClinicalSymptomsDepressionCreate(CreateView):
    model = SymptomsDepression
    template_name = 'clinical/clinical-sub-create.html'
    form_class = SymptomsDepressionForm

    def get_initial(self, *args, **kwargs):
        studyparticipant = None
        if (self.kwargs):
            pid = self.kwargs.get('clinicalid')
            studyparticipant = Clinical.objects.get(pk=pid)
        initial = super(ClinicalSymptomsDepressionCreate, self).get_initial(**kwargs)
        initial['title'] = 'Create Clinical Depression Symptoms Record'
        initial['participant'] = studyparticipant
        return initial

    def get_success_url(self):
        return reverse('clinical_detail', args=[self.object.participant.id])


class ClinicalSymptomsDepressionUpdate(UpdateView):
    model = SymptomsDepression
    template_name = 'clinical/clinical-sub-create.html'
    form_class = SymptomsDepressionForm

    def get_initial(self, *args, **kwargs):
        initial = super(ClinicalSymptomsDepressionUpdate, self).get_initial(**kwargs)
        initial['title'] = 'Update Clinical Depression Symptoms Record'
        return initial

    def get_success_url(self):
        return reverse('clinical_detail', args=[self.object.participant.id])
