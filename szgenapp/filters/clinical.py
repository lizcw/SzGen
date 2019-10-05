import django_filters

from szgenapp.models.clinical import *
from szgenapp.models.studies import Study


class ClinicalFilter(django_filters.FilterSet):
    participant = django_filters.CharFilter(field_name='participant__fullnumber', lookup_expr='exact')
    participant__contains = django_filters.CharFilter(field_name='participant__fullnumber', lookup_expr='icontains')
    study = django_filters.ModelChoiceFilter(
        field_name='participant__study', label='Study',
        queryset=Study.objects.all())
    diagnosis = django_filters.ChoiceFilter(field_name='diagnosis__summary',
                                            choices=DSMIV_CHOICES, label='Diagnosis')
    gender = django_filters.ChoiceFilter(field_name='demographic__gender',
                                         choices=GENDER_CHOICES, label='Gender')
    age = django_filters.NumberFilter(field_name='demographic__age_assessment', label='Age is exactly')
    age__gt = django_filters.NumberFilter(field_name='demographic__age_assessment', label='Age is greater than', lookup_expr='gt')
    age__lt = django_filters.NumberFilter(field_name='demographic__age_assessment', label='Age is less than', lookup_expr='lt')

    class Meta:
        model = Clinical
        fields = ['participant', 'participant__contains', 'study']


class DemographicFilter(django_filters.FilterSet):
    participant = django_filters.CharFilter(field_name='clinical__participant__fullnumber',
                                            lookup_expr='icontains', label='Participant Full Number'
                                            )
    study = django_filters.ModelChoiceFilter(
        field_name='clinical__participant__study', label='Study',
        queryset=Study.objects.all())

    age = django_filters.NumberFilter(field_name='age_assessment')
    age__gt = django_filters.NumberFilter(field_name='age_assessment', lookup_expr='gt')
    age__lt = django_filters.NumberFilter(field_name='age_assessment', lookup_expr='lt')

    class Meta:
        model = Demographic
        fields = ['participant', 'study', 'gender', 'marital_status', 'living_arr', 'years_school',
                  'current_emp_status', 'employment_history']


class DiagnosisFilter(django_filters.FilterSet):
    participant = django_filters.CharFilter(field_name='clinical__participant__fullnumber',
                                            lookup_expr='icontains', label='Participant Full Number')
    study = django_filters.ModelChoiceFilter(
        field_name='clinical__participant__study', label='Study',
        queryset=Study.objects.all())
    age = django_filters.NumberFilter(field_name='age_onset')
    age__gt = django_filters.NumberFilter(field_name='age_onset', lookup_expr='gt')
    age__lt = django_filters.NumberFilter(field_name='age_onset', lookup_expr='lt')
    ageft = django_filters.NumberFilter(field_name='age_first_treatment')
    ageft__gt = django_filters.NumberFilter(field_name='age_first_treatment', lookup_expr='gt')
    ageft__lt = django_filters.NumberFilter(field_name='age_first_treatment', lookup_expr='lt')
    illness = django_filters.NumberFilter(field_name='illness_duration')
    illness__gt = django_filters.NumberFilter(field_name='illness_duration', lookup_expr='gt')
    illness__lt = django_filters.NumberFilter(field_name='illness_duration', lookup_expr='lt')
    dup = django_filters.NumberFilter(field_name='dup')
    dup__gt = django_filters.NumberFilter(field_name='dup', lookup_expr='gt')
    dup__lt = django_filters.NumberFilter(field_name='dup', lookup_expr='lt')
    hospitalisations = django_filters.NumberFilter(field_name='hospitalisation_number')
    hospitalisations__gt = django_filters.NumberFilter(field_name='hospitalisation_number', lookup_expr='gt')
    hospitalisations__lt = django_filters.NumberFilter(field_name='hospitalisation_number', lookup_expr='lt')

    class Meta:
        model = Diagnosis
        fields = ['participant', 'study', 'summary', 'hospitalisation']


class MedicalHistoryFilter(django_filters.FilterSet):
    participant = django_filters.CharFilter(field_name='clinical__participant__fullnumber',
                                            lookup_expr='icontains', label='Participant Full Number')
    study = django_filters.ModelChoiceFilter(
        field_name='clinical__participant__study', label='Study',
        queryset=Study.objects.all())
    other_drug_type = django_filters.CharFilter(field_name='other_drug_type',
                                                lookup_expr='icontains', label='Illicit drug use disorder')

    class Meta:
        model = MedicalHistory
        fields = ['participant', 'study', 'thyroid', 'epilepsy', 'head_injury', 'abnormal_bed',
                  'intellectual_disability', 'alcohol', 'cannabis', 'other_drug',
                  'suicide', 'suicide_serious']


class SymptomsGeneralFilter(django_filters.FilterSet):
    participant = django_filters.CharFilter(field_name='clinical__participant__fullnumber',
                                            lookup_expr='icontains', label='Participant Full Number')
    study = django_filters.ModelChoiceFilter(
        field_name='clinical__participant__study', label='Study',
        queryset=Study.objects.all())

    class Meta:
        model = SymptomsGeneral
        fields = ['participant', 'study', 'onset', 'severity_pattern', 'symptom_pattern', 'illness_course', 'curr_gaf',
                  'wl_gaf', 'current_ap_medication', 'clozapine_status', 'treatment_resistant']


class SymptomsDelusionFilter(django_filters.FilterSet):
    participant = django_filters.CharFilter(field_name='clinical__participant__fullnumber',
                                            lookup_expr='icontains', label='Participant Full Number')
    study = django_filters.ModelChoiceFilter(
        field_name='clinical__participant__study', label='Study',
        queryset=Study.objects.all())

    class Meta:
        model = SymptomsDelusion
        fields = ['participant', 'study', 'final_delusions', 'sevcur_delusions', 'bizarre_delusions', 'biw_delusions',
                  'control_delusions', 'persecutory_delusions', 'reference_delusions', 'jealousy_delusions',
                  'guilt_sin_delusions', 'grandiose_delusions', 'religious_delusions', 'somatic_delusions',
                  'eroto_delusions', 'mindread_delusions']


class SymptomsHallucinationFilter(django_filters.FilterSet):
    participant = django_filters.CharFilter(field_name='clinical__participant__fullnumber',
                                            lookup_expr='icontains', label='Participant Full Number')
    study = django_filters.ModelChoiceFilter(
        field_name='clinical__participant__study', label='Study',
        queryset=Study.objects.all())

    class Meta:
        model = SymptomsHallucination
        fields = ['participant', 'study', 'final_hallucinations', 'severe_hallucinations', 'auditory_hallucinations',
                  'auditory_commentary_hallucinations', 'visual_hallucinations', 'olf_gust_hallucinations',
                  'somatic_hallucinations']


class SymptomsBehaviourFilter(django_filters.FilterSet):
    participant = django_filters.CharFilter(field_name='clinical__participant__fullnumber',
                                            lookup_expr='icontains', label='Participant Full Number')
    study = django_filters.ModelChoiceFilter(
        field_name='clinical__participant__study', label='Study',
        queryset=Study.objects.all())

    class Meta:
        model = SymptomsBehaviour
        fields = ['participant', 'study', 'disorg_speech', 'severe_disorg_speech', 'disorg_catatonic_behav',
                  'severe_disorg_catatonic_behav', 'negative_symptoms', 'affective_flattening',
                  'allogia', 'avolition', 'anhedonia']


class SymptomsDepressionFilter(django_filters.FilterSet):
    participant = django_filters.CharFilter(field_name='clinical__participant__fullnumber',
                                            lookup_expr='icontains', label='Participant Full Number')
    study = django_filters.ModelChoiceFilter(
        field_name='clinical__participant__study', label='Study',
        queryset=Study.objects.all())
    depressive_symptoms_count = django_filters.NumberFilter(field_name='depressive_symptoms_count')
    depressive_symptoms_count__gt = django_filters.NumberFilter(field_name='depressive_symptoms_count',
                                                                lookup_expr='gt')
    depressive_symptoms_count__lt = django_filters.NumberFilter(field_name='depressive_symptoms_count',
                                                                lookup_expr='lt')

    class Meta:
        model = SymptomsDepression
        fields = ['participant', 'study', 'final_depression', 'depressed_mood', 'depression_anhedonia',
                  'app_wt_change', 'sleep_disturb', 'psych_change',
                  'fatigue_energyloss', 'worthless_guilt', 'decreased_conc', 'death_suicide']


class SymptomsManiaFilter(django_filters.FilterSet):
    participant = django_filters.CharFilter(field_name='clinical__participant__fullnumber',
                                            lookup_expr='icontains', label='Participant Full Number')
    study = django_filters.ModelChoiceFilter(
        field_name='clinical__participant__study', label='Study',
        queryset=Study.objects.all())
    manic_count = django_filters.NumberFilter(field_name='manic_count')
    manic_count__gt = django_filters.NumberFilter(field_name='manic_count', lookup_expr='gt')
    manic_count__lt = django_filters.NumberFilter(field_name='manic_count', lookup_expr='lt')

    class Meta:
        model = SymptomsMania
        fields = ['participant', 'study', 'final_mania', 'elevated_mood', 'irritable_mood',
                  'grandiosity', 'decreased_sleep', 'pressured_speech',
                  'racing_thoughts', 'distractibility', 'psychmotor_agitation', 'risky_behaviour']
