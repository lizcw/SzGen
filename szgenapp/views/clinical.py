from django.db import IntegrityError, transaction
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView
from django_filters.views import FilterView
from django_tables2.export.views import ExportMixin
from django_tables2.views import SingleTableMixin
from django.core.exceptions import ValidationError

from szgenapp.filters import *
from szgenapp.forms.clinical import *
from szgenapp.models.participants import StudyParticipant
from szgenapp.tables import *


class ClinicalDetail(DetailView):
    model = Clinical
    template_name = 'clinical/clinical.html'
    context_object_name = 'clinical'


class ClinicalList(SingleTableMixin, ExportMixin, FilterView):
    """
    List of top level Clinical records with filters and export
    """
    model = Clinical
    template_name = 'clinical/clinical-list.html'
    paginate_by = 10
    filterset_class = ClinicalFilter
    table_class = ClinicalTable

    def get_context_data(self, **kwargs):
        data = super(ClinicalList, self).get_context_data(**kwargs)
        data['title'] = 'Summary'
        studyid = self.kwargs.get('study')
        if studyid is not None:
            study = Study.objects.get(pk=studyid)
            data['title'] += ' for ' + study.title
        return data

    def get_queryset(self, **kwargs):
        study = self.kwargs.get('study')
        if study is None:
            qs = Clinical.objects.all()
        else:
            qs = Clinical.objects.filter(participant__study__id=study)

        return qs


class ClinicalDemographicList(SingleTableMixin, FilterView):
    model = Demographic
    table_class = DemographicTable
    paginate_by = 10
    filterset_class = DemographicFilter
    template_name = 'clinical/clinical-list.html'

    def get_context_data(self, **kwargs):
        data = super(ClinicalDemographicList, self).get_context_data(**kwargs)
        data['title'] = 'Demographics'
        return data


class ClinicalDiagnosisList(SingleTableMixin, FilterView):
    model = Diagnosis
    table_class = DiagnosisTable
    paginate_by = 10
    filterset_class = DiagnosisFilter
    template_name = 'clinical/clinical-list.html'

    def get_context_data(self, **kwargs):
        data = super(ClinicalDiagnosisList, self).get_context_data(**kwargs)
        data['title'] = 'Diagnosis'
        return data


class ClinicalMedicalList(SingleTableMixin, FilterView):
    model = MedicalHistory
    table_class = MedicalHistoryTable
    paginate_by = 10
    filterset_class = MedicalHistoryFilter
    template_name = 'clinical/clinical-list.html'

    def get_context_data(self, **kwargs):
        data = super(ClinicalMedicalList, self).get_context_data(**kwargs)
        data['title'] = 'Medical History'
        return data


class ClinicalSymptomsGeneralList(SingleTableMixin, FilterView):
    model = SymptomsGeneral
    table_class = SymptomsGeneralTable
    paginate_by = 10
    filterset_class = SymptomsGeneralFilter
    template_name = 'clinical/clinical-list.html'

    def get_context_data(self, **kwargs):
        data = super(ClinicalSymptomsGeneralList, self).get_context_data(**kwargs)
        data['title'] = 'General Symptoms'
        return data


class ClinicalSymptomsDelusionList(SingleTableMixin, FilterView):
    model = SymptomsDelusion
    table_class = SymptomsDelusionTable
    paginate_by = 10
    filterset_class = SymptomsDelusionFilter
    template_name = 'clinical/clinical-list.html'

    def get_context_data(self, **kwargs):
        data = super(ClinicalSymptomsDelusionList, self).get_context_data(**kwargs)
        data['title'] = 'Delusion Symptoms'
        return data


class ClinicalSymptomsHallucinationList(SingleTableMixin, FilterView):
    model = SymptomsHallucination
    table_class = SymptomsHallucinationTable
    paginate_by = 10
    filterset_class = SymptomsHallucinationFilter
    template_name = 'clinical/clinical-list.html'

    def get_context_data(self, **kwargs):
        data = super(ClinicalSymptomsHallucinationList, self).get_context_data(**kwargs)
        data['title'] = 'Hallucination Symptoms'
        return data


class ClinicalSymptomsBehaviourList(SingleTableMixin, FilterView):
    model = SymptomsBehaviour
    table_class = SymptomsBehaviourTable
    paginate_by = 10
    filterset_class = SymptomsBehaviourFilter
    template_name = 'clinical/clinical-list.html'

    def get_context_data(self, **kwargs):
        data = super(ClinicalSymptomsBehaviourList, self).get_context_data(**kwargs)
        data['title'] = 'Behaviour Symptoms'
        return data


class ClinicalSymptomsDepressionList(SingleTableMixin, FilterView):
    model = SymptomsDepression
    table_class = SymptomsDepressionTable
    paginate_by = 10
    filterset_class = SymptomsDepressionFilter
    template_name = 'clinical/clinical-list.html'

    def get_context_data(self, **kwargs):
        data = super(ClinicalSymptomsDepressionList, self).get_context_data(**kwargs)
        data['title'] = 'Depression Symptoms'
        return data


class ClinicalSymptomsManiaList(SingleTableMixin, FilterView):
    model = SymptomsMania
    table_class = SymptomsManiaTable
    paginate_by = 10
    filterset_class = SymptomsManiaFilter
    template_name = 'clinical/clinical-list.html'

    def get_context_data(self, **kwargs):
        data = super(ClinicalSymptomsManiaList, self).get_context_data(**kwargs)
        data['title'] = 'Mania Symptoms'
        return data


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
            data['symptoms_hallucination'] = SymptomsHallucinationFormset(self.request.POST)
            data['symptoms_behaviour'] = SymptomsBehaviourFormset(self.request.POST)
            data['symptoms_depression'] = SymptomsDepressionFormset(self.request.POST)
            data['symptoms_mania'] = SymptomsManiaFormset(self.request.POST)
        else:
            data['demographic'] = DemographicFormset()
            data['diagnosis'] = DiagnosisFormset()
            data['medical'] = MedicalHistoryFormset()
            data['symptoms_general'] = SymptomsGeneralFormset()
            data['symptoms_delusion'] = SymptomsDelusionFormset()
            data['symptoms_hallucination'] = SymptomsHallucinationFormset()
            data['symptoms_behaviour'] = SymptomsBehaviourFormset()
            data['symptoms_depression'] = SymptomsDepressionFormset()
            data['symptoms_mania'] = SymptomsManiaFormset()
        data['tablist'] = [(key, key.replace('_', ': ').upper()) for key in data.keys() if key != 'form' and
                           key != 'view' and key != 'title' and key != 'object' and key != 'clinical']
        return data

    def form_valid(self, form):
        try:
            context = self.get_context_data()
            demographic = context['demographic']
            diagnosis = context['diagnosis']
            medical = context['medical']
            symptoms_general = context['symptoms_general']
            symptoms_delusion = context['symptoms_delusion']
            symptoms_hallucination = context['symptoms_hallucination']
            symptoms_behaviour = context['symptoms_behaviour']
            symptoms_depression = context['symptoms_depression']
            symptoms_mania = context['symptoms_mania']
            # with transaction.atomic():
            #     self.object = form.save(commit=False)
            # if form.initial['participant']:
            #     self.object.participant = form.initial['participant']
            # Add additional subforms
            if demographic.is_valid():
                form.instance.demographic = demographic.save()
                # self.object.instance.clinical_demographic = demographic.save()
            if diagnosis.is_valid():
                form.instance.diagnosis = diagnosis.save()
            if medical.is_valid():
                form.instance.medical = medical.save()
            if symptoms_general.is_valid():
                form.instance.symptoms_general = symptoms_general.save()
            if symptoms_delusion.is_valid():
                form.instance.symptoms_delusion = symptoms_delusion.save()
            if symptoms_depression.is_valid():
                form.instance.symptoms_depression = symptoms_depression.save()
            if symptoms_hallucination.is_valid():
                form.instance.symptoms_hallucination = symptoms_hallucination.save()
            if symptoms_behaviour.is_valid():
                form.instance.symptoms_behaviour = symptoms_behaviour.save()
            if symptoms_mania.is_valid():
                form.instance.symptoms_mania = symptoms_mania.save()
            # final commit
            # self.object.save()
            self.object = form.save()
            return super(ClinicalCreate, self).form_valid(form)
        except IntegrityError as e:
            msg = 'Database Error: Unable to create Clinical Record - see Administrator: %s' % e
            form.add_error('participant', msg)
            print('ERROR: ', msg)
            return self.form_invalid(form)
        except ValidationError as v:
            msg = 'Validation Error: Unable to create Clinical Record - see Administrator: %s' % v
            form.add_error('participant', msg)
            print('ERROR: ', msg)
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse('clinical_detail', args=[self.object.id])


class ClinicalUpdate(UpdateView):
    model = Clinical
    template_name = 'clinical/clinical-create.html'
    form_class = ClinicalForm

    def get_initial(self, *args, **kwargs):
        initial = super(ClinicalUpdate, self).get_initial()
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
            data['symptoms_hallucination'] = SymptomsHallucinationFormset(self.request.POST)
            data['symptoms_behaviour'] = SymptomsBehaviourFormset(self.request.POST)
            data['symptoms_depression'] = SymptomsDepressionFormset(self.request.POST)
            data['symptoms_mania'] = SymptomsManiaFormset(self.request.POST)
        else:
            data['demographic'] = DemographicFormset(instance=self.get_object().demographic)
            data['diagnosis'] = DiagnosisFormset(instance=self.get_object().diagnosis)
            data['medical'] = MedicalHistoryFormset(instance=self.get_object().medical)
            data['symptoms_general'] = SymptomsGeneralFormset(instance=self.get_object().symptoms_general)
            data['symptoms_delusion'] = SymptomsDelusionFormset(instance=self.get_object().symptoms_delusion)
            data['symptoms_hallucination'] = SymptomsHallucinationFormset(
                instance=self.get_object().symptoms_hallucination)
            data['symptoms_behaviour'] = SymptomsBehaviourFormset(instance=self.get_object().symptoms_behaviour)
            data['symptoms_depression'] = SymptomsDepressionFormset(instance=self.get_object().symptoms_depression)
            data['symptoms_mania'] = SymptomsManiaFormset(instance=self.get_object().symptoms_mania)
        data['tablist'] = [(key, key.replace('_', ': ').upper()) for key in data.keys() if key != 'form' and
                           key != 'view' and key != 'title' and key != 'object' and key != 'clinical']
        return data

    def get_success_url(self):
        return reverse('clinical_detail', args=[self.object.participant.id])


class ClinicalDelete(DeleteView):
    """
    Delete a clinical record with all subsets
    """
    model = Clinical
    success_url = reverse_lazy('clinical_list')
    template_name = 'clinical/clinical-confirm-delete.html'


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


class ClinicalSymptomsManiaCreate(CreateView):
    model = SymptomsMania
    template_name = 'clinical/clinical-sub-create.html'
    form_class = SymptomsManiaForm

    def get_initial(self, *args, **kwargs):
        studyparticipant = None
        if (self.kwargs):
            pid = self.kwargs.get('clinicalid')
            studyparticipant = Clinical.objects.get(pk=pid)
        initial = super(ClinicalSymptomsManiaCreate, self).get_initial(**kwargs)
        initial['title'] = 'Create Clinical Mania Symptoms Record'
        initial['participant'] = studyparticipant
        return initial

    def get_success_url(self):
        return reverse('clinical_detail', args=[self.object.clinical_mania.get().id])


class ClinicalSymptomsManiaUpdate(UpdateView):
    model = SymptomsMania
    template_name = 'clinical/clinical-sub-create.html'
    form_class = SymptomsManiaForm

    def get_initial(self, *args, **kwargs):
        initial = super(ClinicalSymptomsManiaUpdate, self).get_initial(**kwargs)
        initial['title'] = 'Update Clinical Mania Symptoms Record'
        return initial

    def get_success_url(self):
        return reverse('clinical_detail', args=[self.object.clinical_mania.get().id])
