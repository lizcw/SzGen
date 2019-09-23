import logging

from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView
from django_filters.views import FilterView
from django_tables2.export.views import ExportMixin
from django_tables2.views import SingleTableMixin
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from szgenapp.filters import *
from szgenapp.forms.clinical import *
from szgenapp.tables import *

logger = logging.getLogger(__name__)


class ClinicalDetail(LoginRequiredMixin, DetailView):
    model = Clinical
    template_name = 'clinical/clinical.html'
    context_object_name = 'clinical'


class ClinicalList(LoginRequiredMixin, SingleTableMixin, ExportMixin, FilterView):
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
        data['reset_url'] = 'clinical_list'
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

        return qs.order_by('id')


class ClinicalDemographicList(LoginRequiredMixin, SingleTableMixin, FilterView):
    model = Demographic
    table_class = DemographicTable
    paginate_by = 10
    filterset_class = DemographicFilter
    template_name = 'clinical/clinical-list.html'

    def get_context_data(self, **kwargs):
        data = super(ClinicalDemographicList, self).get_context_data(**kwargs)
        data['title'] = 'Demographics'
        data['reset_url'] = 'clinical_demographic_list'
        return data


class ClinicalDiagnosisList(LoginRequiredMixin, SingleTableMixin, FilterView):
    model = Diagnosis
    table_class = DiagnosisTable
    paginate_by = 10
    filterset_class = DiagnosisFilter
    template_name = 'clinical/clinical-list.html'

    def get_context_data(self, **kwargs):
        data = super(ClinicalDiagnosisList, self).get_context_data(**kwargs)
        data['title'] = 'Diagnosis'
        data['reset_url'] = 'clinical_diagnosis_list'
        return data


class ClinicalMedicalList(LoginRequiredMixin, SingleTableMixin, FilterView):
    model = MedicalHistory
    table_class = MedicalHistoryTable
    paginate_by = 10
    filterset_class = MedicalHistoryFilter
    template_name = 'clinical/clinical-list.html'

    def get_context_data(self, **kwargs):
        data = super(ClinicalMedicalList, self).get_context_data(**kwargs)
        data['title'] = 'Medical History'
        data['reset_url'] = 'clinical_medical_list'
        return data


class ClinicalSymptomsGeneralList(LoginRequiredMixin, SingleTableMixin, FilterView):
    model = SymptomsGeneral
    table_class = SymptomsGeneralTable
    paginate_by = 10
    filterset_class = SymptomsGeneralFilter
    template_name = 'clinical/clinical-list.html'

    def get_context_data(self, **kwargs):
        data = super(ClinicalSymptomsGeneralList, self).get_context_data(**kwargs)
        data['title'] = 'General Symptoms'
        data['reset_url'] = 'clinical_symptoms_general_list'
        return data


class ClinicalSymptomsDelusionList(LoginRequiredMixin, SingleTableMixin, FilterView):
    model = SymptomsDelusion
    table_class = SymptomsDelusionTable
    paginate_by = 10
    filterset_class = SymptomsDelusionFilter
    template_name = 'clinical/clinical-list.html'

    def get_context_data(self, **kwargs):
        data = super(ClinicalSymptomsDelusionList, self).get_context_data(**kwargs)
        data['title'] = 'Delusion Symptoms'
        data['reset_url'] = 'clinical_symptoms_delusion_list'
        return data


class ClinicalSymptomsHallucinationList(LoginRequiredMixin, SingleTableMixin, FilterView):
    model = SymptomsHallucination
    table_class = SymptomsHallucinationTable
    paginate_by = 10
    filterset_class = SymptomsHallucinationFilter
    template_name = 'clinical/clinical-list.html'

    def get_context_data(self, **kwargs):
        data = super(ClinicalSymptomsHallucinationList, self).get_context_data(**kwargs)
        data['title'] = 'Hallucination Symptoms'
        data['reset_url'] = 'clinical_symptoms_hallucination_list'
        return data


class ClinicalSymptomsBehaviourList(LoginRequiredMixin, SingleTableMixin, FilterView):
    model = SymptomsBehaviour
    table_class = SymptomsBehaviourTable
    paginate_by = 10
    filterset_class = SymptomsBehaviourFilter
    template_name = 'clinical/clinical-list.html'

    def get_context_data(self, **kwargs):
        data = super(ClinicalSymptomsBehaviourList, self).get_context_data(**kwargs)
        data['title'] = 'Behaviour Symptoms'
        data['reset_url'] = 'clinical_symptoms_behaviour_list'
        return data


class ClinicalSymptomsDepressionList(LoginRequiredMixin, SingleTableMixin, FilterView):
    model = SymptomsDepression
    table_class = SymptomsDepressionTable
    paginate_by = 10
    filterset_class = SymptomsDepressionFilter
    template_name = 'clinical/clinical-list.html'

    def get_context_data(self, **kwargs):
        data = super(ClinicalSymptomsDepressionList, self).get_context_data(**kwargs)
        data['title'] = 'Depression Symptoms'
        data['reset_url'] = 'clinical_symptoms_depression_list'
        return data


class ClinicalSymptomsManiaList(LoginRequiredMixin, SingleTableMixin, FilterView):
    model = SymptomsMania
    table_class = SymptomsManiaTable
    paginate_by = 10
    filterset_class = SymptomsManiaFilter
    template_name = 'clinical/clinical-list.html'

    def get_context_data(self, **kwargs):
        data = super(ClinicalSymptomsManiaList, self).get_context_data(**kwargs)
        data['title'] = 'Mania Symptoms'
        data['reset_url'] = 'clinical_symptoms_mania_list'
        return data


class ClinicalCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Clinical
    template_name = 'clinical/clinical-create.html'
    form_class = ClinicalForm
    permission_required = 'szgenapp.add_clinical'

    def get_initial(self, *args, **kwargs):
        initial = super(ClinicalCreate, self).get_initial(**kwargs)
        pid = self.kwargs.get('participantid')
        if pid is not None:
            studyparticipant = StudyParticipant.objects.get(pk=pid)
            initial['participant'] = studyparticipant
        initial['action'] = 'Create'
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
        data['tablist'] = [(key, key.replace('_', ': ').upper()) for key in data.keys() if
                           key not in ['form', 'view', 'title', 'object', 'clinical', 'participant']]
        return data

    def form_valid(self, form):
        try:
            context = self.get_context_data()

            if form.is_valid():
                with transaction.atomic():
                    self.object = form.save()
            else:
                raise ValidationError('Clinical form is not valid')
            for subset in CLINICAL_SUBSETS:
                subform = context[subset]
                if subform.is_valid():
                    subform.instance = self.object
                    subform.save()
                else:
                    msg = '%s form is not valid' % subform
                    raise ValidationError(msg)

            return super(ClinicalCreate, self).form_valid(form)
        except IntegrityError as e:
            msg = 'Database Error: Unable to create Clinical Record: %s' % e
            form.add_error(None, msg)
            logger.error(msg)
            return self.form_invalid(form)
        except ValidationError as v:
            msg = 'Validation Error: Unable to create Clinical Record: %s' % v
            form.add_error(None, msg)
            logger.error(msg)
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse('clinical_detail', args=[self.object.id])


class ClinicalDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """
    Delete a clinical record with all subsets
    """
    model = Clinical
    success_url = reverse_lazy('clinical_list')
    template_name = 'clinical/clinical-confirm-delete.html'
    permission_required = 'szgenapp.delete_clinical'


class ClinicalDemographicCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Demographic
    template_name = 'clinical/clinical-sub-create.html'
    form_class = DemographicForm
    permission_required = 'szgenapp.add_demographic'

    def get_initial(self, *args, **kwargs):
        initial = super(ClinicalDemographicCreate, self).get_initial(**kwargs)
        if self.kwargs:
            pid = self.kwargs.get('clinicalid')
            initial['clinical'] = Clinical.objects.get(pk=pid)
        initial['title'] = 'Create Clinical Demographic Record'
        return initial

    def get_success_url(self):
        return reverse('clinical_detail', args=[self.object.clinical.id])


class ClinicalDemographicUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Demographic
    template_name = 'clinical/clinical-sub-create.html'
    form_class = DemographicForm
    permission_required = 'szgenapp.change_demographic'

    def get_initial(self, *args, **kwargs):
        initial = super(ClinicalDemographicUpdate, self).get_initial(**kwargs)
        initial['title'] = 'Update Clinical Demographic Record'
        initial['clinical'] = self.get_object().clinical
        return initial

    def get_success_url(self):
        return reverse('clinical_detail', args=[self.object.clinical.id])


class ClinicalDiagnosisCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Diagnosis
    template_name = 'clinical/clinical-sub-create.html'
    form_class = DiagnosisForm
    permission_required = 'szgenapp.add_diagnosis'

    def get_initial(self, *args, **kwargs):
        initial = super(self.__class__, self).get_initial(**kwargs)
        if self.kwargs:
            pid = self.kwargs.get('clinicalid')
            initial['clinical'] = Clinical.objects.get(pk=pid)
        initial['title'] = 'Create Clinical Diagnosis Record'
        return initial

    def get_success_url(self):
        return reverse('clinical_detail', args=[self.object.clinical.id])


class ClinicalDiagnosisUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Diagnosis
    template_name = 'clinical/clinical-sub-create.html'
    form_class = DiagnosisForm
    permission_required = 'szgenapp.change_diagnosis'

    def get_initial(self, *args, **kwargs):
        initial = super(ClinicalDiagnosisUpdate, self).get_initial(**kwargs)
        initial['title'] = 'Update Clinical Diagnosis Record'
        initial['clinical'] = self.get_object().clinical
        return initial

    def get_success_url(self):
        return reverse('clinical_detail', args=[self.object.clinical.id])


class ClinicalMedicalCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = MedicalHistory
    template_name = 'clinical/clinical-sub-create.html'
    form_class = MedicalHistoryForm
    permission_required = 'szgenapp.add_medicalhistory'

    def get_initial(self, *args, **kwargs):
        initial = super(self.__class__, self).get_initial(**kwargs)
        if self.kwargs:
            pid = self.kwargs.get('clinicalid')
            initial['clinical'] = Clinical.objects.get(pk=pid)
        initial['title'] = 'Create Clinical Medical Record'
        return initial

    def get_success_url(self):
        return reverse('clinical_detail', args=[self.object.clinical.id])


class ClinicalMedicalUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = MedicalHistory
    template_name = 'clinical/clinical-sub-create.html'
    form_class = MedicalHistoryForm
    permission_required = 'szgenapp.change_medicalhistory'

    def get_initial(self, *args, **kwargs):
        initial = super(ClinicalMedicalUpdate, self).get_initial(**kwargs)
        initial['title'] = 'Update Clinical Medical Record'
        initial['clinical'] = self.get_object().clinical
        return initial

    def get_success_url(self):
        return reverse('clinical_detail', args=[self.object.clinical.id])


class ClinicalSymptomsGeneralCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = SymptomsGeneral
    template_name = 'clinical/clinical-sub-create.html'
    form_class = SymptomsGeneralForm
    permission_required = 'szgenapp.add_symptomsgeneral'

    def get_initial(self, *args, **kwargs):
        initial = super(self.__class__, self).get_initial(**kwargs)
        if self.kwargs:
            pid = self.kwargs.get('clinicalid')
            initial['clinical'] = Clinical.objects.get(pk=pid)
        initial['title'] = 'Create Clinical General Symptoms Record'
        return initial

    def get_success_url(self):
        return reverse('clinical_detail', args=[self.object.clinical.id])


class ClinicalSymptomsGeneralUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = SymptomsGeneral
    template_name = 'clinical/clinical-sub-create.html'
    form_class = SymptomsGeneralForm
    permission_required = 'szgenapp.change_symptomsgeneral'

    def get_initial(self, *args, **kwargs):
        initial = super(ClinicalSymptomsGeneralUpdate, self).get_initial(**kwargs)
        initial['title'] = 'Update Clinical General Symptoms Record'
        initial['clinical'] = self.get_object().clinical
        return initial

    def get_success_url(self):
        return reverse('clinical_detail', args=[self.object.clinical.id])


class ClinicalSymptomsDelusionCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = SymptomsDelusion
    template_name = 'clinical/clinical-sub-create.html'
    form_class = SymptomsDelusionForm
    permission_required = 'szgenapp.add_symptomsdelusion'

    def get_initial(self, *args, **kwargs):
        initial = super(self.__class__, self).get_initial(**kwargs)
        if self.kwargs:
            pid = self.kwargs.get('clinicalid')
            initial['clinical'] = Clinical.objects.get(pk=pid)
        initial['title'] = 'Create Clinical Delusion Symptoms Record'
        initial['clinical'] = self.get_object().clinical
        return initial

    def get_success_url(self):
        return reverse('clinical_detail', args=[self.object.clinical.id])


class ClinicalSymptomsDelusionUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = SymptomsDelusion
    template_name = 'clinical/clinical-sub-create.html'
    form_class = SymptomsDelusionForm
    permission_required = 'szgenapp.change_symptomsdelusion'

    def get_initial(self, *args, **kwargs):
        initial = super(ClinicalSymptomsDelusionUpdate, self).get_initial(**kwargs)
        initial['title'] = 'Update Clinical Delusion Symptoms Record'
        initial['clinical'] = self.get_object().clinical
        return initial

    def get_success_url(self):
        return reverse('clinical_detail', args=[self.object.clinical.id])


class ClinicalSymptomsHallucinationCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = SymptomsHallucination
    template_name = 'clinical/clinical-sub-create.html'
    form_class = SymptomsHallucinationForm
    permission_required = 'szgenapp.add_symptomshallucination'

    def get_initial(self, *args, **kwargs):
        initial = super(self.__class__, self).get_initial(**kwargs)
        if self.kwargs:
            pid = self.kwargs.get('clinicalid')
            initial['clinical'] = Clinical.objects.get(pk=pid)
        initial['title'] = 'Create Clinical Hallucination Symptoms Record'
        return initial

    def get_success_url(self):
        return reverse('clinical_detail', args=[self.object.clinical.id])


class ClinicalSymptomsHallucinationUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = SymptomsHallucination
    template_name = 'clinical/clinical-sub-create.html'
    form_class = SymptomsHallucinationForm
    permission_required = 'szgenapp.change_symptomshallucination'

    def get_initial(self, *args, **kwargs):
        initial = super(ClinicalSymptomsHallucinationUpdate, self).get_initial(**kwargs)
        initial['title'] = 'Update Clinical Hallucination Symptoms Record'
        initial['clinical'] = self.get_object().clinical
        return initial

    def get_success_url(self):
        return reverse('clinical_detail', args=[self.object.clinical.id])


class ClinicalSymptomsBehaviourCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = SymptomsBehaviour
    template_name = 'clinical/clinical-sub-create.html'
    form_class = SymptomsBehaviourForm
    permission_required = 'szgenapp.add_symptomsbehaviour'

    def get_initial(self, *args, **kwargs):
        initial = super(self.__class__, self).get_initial(**kwargs)
        if self.kwargs:
            pid = self.kwargs.get('clinicalid')
            initial['clinical'] = Clinical.objects.get(pk=pid)
        initial['title'] = 'Create Clinical Behaviour Symptoms Record'
        return initial

    def get_success_url(self):
        return reverse('clinical_detail', args=[self.object.clinical.id])


class ClinicalSymptomsBehaviourUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = SymptomsBehaviour
    template_name = 'clinical/clinical-sub-create.html'
    form_class = SymptomsBehaviourForm
    permission_required = 'szgenapp.change_symptomsbehaviour'

    def get_initial(self, *args, **kwargs):
        initial = super(ClinicalSymptomsBehaviourUpdate, self).get_initial(**kwargs)
        initial['title'] = 'Update Clinical Behaviour Symptoms Record'
        initial['clinical'] = self.get_object().clinical
        return initial

    def get_success_url(self):
        return reverse('clinical_detail', args=[self.object.clinical.id])


class ClinicalSymptomsDepressionCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = SymptomsDepression
    template_name = 'clinical/clinical-sub-create.html'
    form_class = SymptomsDepressionForm
    permission_required = 'szgenapp.add_symptomsdepression'

    def get_initial(self, *args, **kwargs):
        initial = super(self.__class__, self).get_initial(**kwargs)
        if self.kwargs:
            pid = self.kwargs.get('clinicalid')
            initial['clinical'] = Clinical.objects.get(pk=pid)
        initial['title'] = 'Create Clinical Depression Symptoms Record'
        return initial

    def get_success_url(self):
        return reverse('clinical_detail', args=[self.object.clinical.id])


class ClinicalSymptomsDepressionUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = SymptomsDepression
    template_name = 'clinical/clinical-sub-create.html'
    form_class = SymptomsDepressionForm
    permission_required = 'szgenapp.change_symptomsdepression'

    def get_initial(self, *args, **kwargs):
        initial = super(ClinicalSymptomsDepressionUpdate, self).get_initial(**kwargs)
        initial['title'] = 'Update Clinical Depression Symptoms Record'
        initial['clinical'] = self.get_object().clinical
        return initial

    def get_success_url(self):
        return reverse('clinical_detail', args=[self.object.clinical.id])


class ClinicalSymptomsManiaCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = SymptomsMania
    template_name = 'clinical/clinical-sub-create.html'
    form_class = SymptomsManiaForm
    permission_required = 'szgenapp.add_symptomsmania'

    def get_initial(self, *args, **kwargs):
        initial = super(self.__class__, self).get_initial(**kwargs)
        if self.kwargs:
            pid = self.kwargs.get('clinicalid')
            initial['clinical'] = Clinical.objects.get(pk=pid)
        initial['title'] = 'Create Clinical Mania Symptoms Record'
        return initial

    def get_success_url(self):
        return reverse('clinical_detail', args=[self.object.clinical.id])


class ClinicalSymptomsManiaUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = SymptomsMania
    template_name = 'clinical/clinical-sub-create.html'
    form_class = SymptomsManiaForm
    permission_required = 'szgenapp.change_symptomsmania'

    def get_initial(self, *args, **kwargs):
        initial = super(ClinicalSymptomsManiaUpdate, self).get_initial(**kwargs)
        initial['title'] = 'Update Clinical Mania Symptoms Record'
        initial['clinical'] = self.get_object().clinical
        return initial

    def get_success_url(self):
        return reverse('clinical_detail', args=[self.object.clinical.id])
