from django.views.generic import CreateView, DetailView, ListView, UpdateView
from django.urls import reverse
from django.db import IntegrityError, transaction
from django.shortcuts import render
from django_tables2 import RequestConfig
from szgenapp.forms.clinical import *
from szgenapp.models.participants import StudyParticipant
from szgenapp.models.clinical import *
from szgenapp.tables import ClinicalTable


class ClinicalDetail(DetailView):
    model = Clinical
    template_name = 'clinical/clinical.html'
    context_object_name = 'clinical'


class ClinicalList(ListView):
    model = Clinical
    template_name = 'clinical/clinical-list.html'
    # queryset = Clinical.objects.all()
    context_object_name = 'clinical'
    paginate_by = 10

    def get_queryset(self):
        table = Clinical.objects.order_by('participant')
        return table

    def get_context_data(self, **kwargs):
        context = super(ClinicalList, self).get_context_data(**kwargs)
        table = ClinicalTable(self.get_queryset())
        RequestConfig(self.request, paginate={"per_page": 20}).configure(table)
        context['table'] = table
        return context



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
                           key != 'view' and key != 'title' and key != 'object' and key != 'clinical']
        return data

    def form_valid(self, form):
        try:
            context=self.get_context_data()
            demographic = context['demographic']
            diagnosis = context['diagnosis']
            medical = context['medical']
            symptoms_general = context['symptoms_general']
            symptoms_delusion = context['symptoms_delusion']
            symptoms_depression = context['symptoms_depression']
            symptoms_hallucination = context['symptoms_hallucination']
            symptoms_behaviour = context['symptoms_behaviour']
            with transaction.atomic():
                self.object = form.save(commit=False)
            if form.initial['participant']:
                self.object.participant = form.initial['participant']
            # Add additional subforms
            if demographic.is_valid():
                self.object.clinical_demographic = demographic.save()
            if diagnosis.is_valid():
                self.object.clinical_diagnosis = diagnosis.save()
            if medical.is_valid():
                self.object.clinical_medical = medical.save()
            if symptoms_general.is_valid():
                self.object.clinical_general = symptoms_general.save()
            if symptoms_delusion.is_valid():
                self.object.clinical_delusion = symptoms_delusion.save()
            if symptoms_depression.is_valid():
                self.object.clinical_depression = symptoms_depression.save()
            if symptoms_hallucination.is_valid():
                self.object.clinical_hallucination = symptoms_hallucination.save()
            if symptoms_behaviour.is_valid():
                self.object.clinical_behaviour = symptoms_behaviour.save()
            # final commit
            self.object.save()
            return super(ClinicalCreate, self).form_valid(form)
        except IntegrityError as e:
            msg = 'Database Error: Unable to create Sample - see Administrator'
            # form.add_error('sample-create', msg)
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse('clinical_detail', args=[self.object.id])


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
            data['demographic'] = DemographicFormset(instance=self.get_object().demographic)
            data['diagnosis'] = DiagnosisFormset(instance=self.get_object().diagnosis)
            data['medical'] = MedicalHistoryFormset(instance=self.get_object().medical)
            data['symptoms_general'] = SymptomsGeneralFormset(instance=self.get_object().symptoms_general)
            data['symptoms_delusion'] = SymptomsDelusionFormset(instance=self.get_object().symptoms_delusion)
            data['symptoms_depression'] = SymptomsDepressionFormset(instance=self.get_object().symptoms_depression)
            data['symptoms_hallucination'] = SymptomsHallucinationFormset(
                instance=self.get_object().symptoms_hallucination)
            data['symptoms_behaviour'] = SymptomsBehaviourFormset(instance=self.get_object().symptoms_behaviour)
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
        return reverse('clinical_detail', args=[self.object.clinical_demographic.get().id])


class ClinicalDemographicUpdate(UpdateView):
    model = Demographic
    template_name = 'clinical/clinical-sub-create.html'
    form_class = DemographicForm

    def get_initial(self, *args, **kwargs):
        initial = super(ClinicalDemographicUpdate, self).get_initial(**kwargs)
        initial['title'] = 'Update Clinical Demographic Record'
        return initial

    def get_success_url(self):
        return reverse('clinical_detail', args=[self.object.clinical_demographic.get().id])


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
        return reverse('clinical_detail', args=[self.object.clinical_diagnosis.get().id])


class ClinicalDiagnosisUpdate(UpdateView):
    model = Diagnosis
    template_name = 'clinical/clinical-sub-create.html'
    form_class = DiagnosisForm

    def get_initial(self, *args, **kwargs):
        initial = super(ClinicalDiagnosisUpdate, self).get_initial(**kwargs)
        initial['title'] = 'Update Clinical Diagnosis Record'
        return initial

    def get_success_url(self):
        return reverse('clinical_detail', args=[self.object.clinical_diagnosis.get().id])


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
        return reverse('clinical_detail', args=[self.object.clinical_medical.get().id])


class ClinicalMedicalUpdate(UpdateView):
    model = MedicalHistory
    template_name = 'clinical/clinical-sub-create.html'
    form_class = MedicalHistoryForm

    def get_initial(self, *args, **kwargs):
        initial = super(ClinicalMedicalUpdate, self).get_initial(**kwargs)
        initial['title'] = 'Update Clinical Medical Record'
        return initial

    def get_success_url(self):
        return reverse('clinical_detail', args=[self.object.clinical_medical.get().id])


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
        return reverse('clinical_detail', args=[self.object.clinical_general.get().id])


class ClinicalSymptomsGeneralUpdate(UpdateView):
    model = SymptomsGeneral
    template_name = 'clinical/clinical-sub-create.html'
    form_class = SymptomsGeneralForm

    def get_initial(self, *args, **kwargs):
        initial = super(ClinicalSymptomsGeneralUpdate, self).get_initial(**kwargs)
        initial['title'] = 'Update Clinical General Symptoms Record'
        return initial

    def get_success_url(self):
        return reverse('clinical_detail', args=[self.object.clinical_general.get().id])


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
        return reverse('clinical_detail', args=[self.object.clinical_delusion.get().id])


class ClinicalSymptomsDelusionUpdate(UpdateView):
    model = SymptomsDelusion
    template_name = 'clinical/clinical-sub-create.html'
    form_class = SymptomsDelusionForm

    def get_initial(self, *args, **kwargs):
        initial = super(ClinicalSymptomsDelusionUpdate, self).get_initial(**kwargs)
        initial['title'] = 'Update Clinical Delusion Symptoms Record'
        return initial

    def get_success_url(self):
        return reverse('clinical_detail', args=[self.object.clinical_delusion.get().id])


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
        return reverse('clinical_detail', args=[self.object.clinical_hallucination.get().id])


class ClinicalSymptomsHallucinationUpdate(UpdateView):
    model = SymptomsHallucination
    template_name = 'clinical/clinical-sub-create.html'
    form_class = SymptomsHallucinationForm

    def get_initial(self, *args, **kwargs):
        initial = super(ClinicalSymptomsHallucinationUpdate, self).get_initial(**kwargs)
        initial['title'] = 'Update Clinical Hallucination Symptoms Record'
        return initial

    def get_success_url(self):
        return reverse('clinical_detail', args=[self.object.clinical_hallucination.get().id])


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
        return reverse('clinical_detail', args=[self.object.clinical_behaviour.get().id])


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
        return reverse('clinical_detail', args=[self.object.clinical_behaviour.get().id])


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
        return reverse('clinical_detail', args=[self.object.clinical_depression.get().id])


class ClinicalSymptomsDepressionUpdate(UpdateView):
    model = SymptomsDepression
    template_name = 'clinical/clinical-sub-create.html'
    form_class = SymptomsDepressionForm

    def get_initial(self, *args, **kwargs):
        initial = super(ClinicalSymptomsDepressionUpdate, self).get_initial(**kwargs)
        initial['title'] = 'Update Clinical Depression Symptoms Record'
        return initial

    def get_success_url(self):
        return reverse('clinical_detail', args=[self.object.clinical_depression.get().id])
