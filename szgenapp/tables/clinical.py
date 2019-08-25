import django_tables2 as tables
from django_tables2.utils import A
from szgenapp.models.clinical import *


# # Generic filtered table
# class FilteredSingleTableView(tables.SingleTableView):
#     filter_class = None
#
#     def get_table_data(self):
#         data = super(FilteredSingleTableView, self).get_table_data()
#         self.filter = self.filter_class(self.request.GET, queryset=data)
#         return self.filter.qs
#
#     def get_context_data(self, **kwargs):
#         context = super(FilteredSingleTableView, self).get_context_data(**kwargs)
#         context['filter'] = self.filter
#         return context



class ClinicalTable(tables.Table):
    id = tables.LinkColumn('clinical_detail', text='View', args=[A('pk')], verbose_name='')
    participant = tables.LinkColumn('participant_detail', args=[A('participant.participant.id')])
    gender = tables.Column(verbose_name='Gender', accessor=A('demographic.gender'))
    diagnosis = tables.Column(verbose_name='Diagnosis', accessor=A('diagnosis.summary'))
    age = tables.Column(verbose_name='Age', accessor=A('demographic.age_assessment'))
    onset = tables.Column(verbose_name='Symptoms onset', accessor=A('symptoms_general.onset'))
    severity_pattern = tables.Column(verbose_name='Symptoms severity', accessor=A('symptoms_general.severity_pattern'))

    class Meta:
        model = Clinical
        template_name = 'django_tables2/bootstrap.html'
        attrs = {"class": "ui-responsive table table-hover"}
        fields = ['id', 'participant']


class DemographicTable(tables.Table):
    participant = tables.LinkColumn('clinical_detail', verbose_name="Participant", accessor=A('clinical_demographic'),
                                    args=[A('pk')])

    def render_participant(self, value):
        """
        Get access to clinical participant via RelatedManager
        :param value:
        :return:
        """
        if value.first():
            participant = value.first().participant
        else:
            participant = 'None'
        return participant

    class Meta:
        model = Demographic
        template_name = 'django_tables2/bootstrap.html'
        attrs = {"class": "ui-responsive table table-hover"}
        fields = ['participant', 'gender', 'age_assessment', 'marital_status', 'living_arr', 'years_school',
                  'current_emp_status', 'employment_history']


class DiagnosisTable(tables.Table):
    participant = tables.LinkColumn('clinical_detail', verbose_name="Participant", accessor=A('clinical_diagnosis'),
                                    args=[A('pk')])

    def render_participant(self, value):
        """
        Get access to clinical participant via RelatedManager
        :param value:
        :return:
        """
        if value.first():
            participant = value.first().participant
        else:
            participant = 'None'
        return participant

    def render_illness_duration(self, value, record):
        """
        Provide approximation char as +
        :param value:
        :param record:
        :return:
        """
        if record.illness_duration_approx:
            value = '%d%s' % (value, '+')
        return value

    def render_dup(self, value, record):
        """
        Provide approximation char as +
        :param value:
        :param record:
        :return:
        """
        if record.dup_approx:
            value = '%d%s' % (value, '+')
        return value

    def render_hospitalisation_number(self, value, record):
        """
        Provide approximation char as >
        :param value:
        :param record:
        :return:
        """
        if record.hospitalisation_number_approx:
            value = '%s%d' % ('>', value)
        return value

    class Meta:
        model = Diagnosis
        template_name = 'django_tables2/bootstrap.html'
        attrs = {"class": "ui-responsive table table-hover"}
        fields = ['participant', 'summary', 'age_onset', 'illness_duration', 'age_first_treatment', 'dup',
                  'hospitalisation', 'hospitalisation_number']


class MedicalHistoryTable(tables.Table):
    participant = tables.LinkColumn('clinical_detail', verbose_name="Participant", accessor=A('clinical_medical'),
                                    args=[A('pk')])

    def render_participant(self, value):
        """
        Get access to clinical participant via RelatedManager
        :param value:
        :return:
        """
        if value.first():
            participant = value.first().participant
        else:
            participant = 'None'
        return participant

    class Meta:
        model = MedicalHistory
        template_name = 'django_tables2/bootstrap.html'
        attrs = {"class": "ui-responsive table table-hover"}
        fields = ['participant', 'thyroid', 'epilepsy', 'head_injury', 'abnormal_bed', 'intellectual_disability',
                  'alcohol', 'cannabis', 'other_drug', 'other_drug_type', 'suicide', 'suicide_serious']


class SymptomsGeneralTable(tables.Table):
    participant = tables.LinkColumn('clinical_detail', verbose_name="Participant", accessor=A('clinical_general'),
                                    args=[A('pk')])

    def render_participant(self, value):
        """
        Get access to clinical participant via RelatedManager
        :param value:
        :return:
        """
        if value.first():
            participant = value.first().participant
        else:
            participant = 'None'
        return participant

    class Meta:
        model = SymptomsGeneral
        template_name = 'django_tables2/bootstrap.html'
        attrs = {"class": "ui-responsive table table-hover"}
        fields = ['participant', 'onset', 'severity_pattern', 'symptom_pattern', 'illness_course', 'curr_gaf',
                  'wl_gaf', 'current_ap_medication', 'clozapine_status', 'treatment_resistant']

class SymptomsDelusionTable(tables.Table):
    participant = tables.LinkColumn('clinical_detail', verbose_name="Participant", accessor=A('clinical_delusion'),
                                    args=[A('pk')])

    def render_participant(self, value):
        """
        Get access to clinical participant via RelatedManager
        :param value:
        :return:
        """
        if value.first():
            participant = value.first().participant
        else:
            participant = 'None'
        return participant

    class Meta:
        model = SymptomsDelusion
        template_name = 'django_tables2/bootstrap.html'
        attrs = {"class": "ui-responsive table table-hover"}
        fields = ['participant', 'final_delusions', 'sevcur_delusions', 'bizarre_delusions', 'biw_delusions',
                  'control_delusions', 'persecutory_delusions', 'reference_delusions', 'jealousy_delusions',
                  'guilt_sin_delusions', 'grandiose_delusions', 'religious_delusions', 'somatic_delusions',
                  'eroto_delusions', 'mindread_delusions']

class SymptomsHallucinationTable(tables.Table):
    participant = tables.LinkColumn('clinical_detail', verbose_name="Participant", accessor=A('clinical_hallucination'),
                                    args=[A('pk')])

    def render_participant(self, value):
        """
        Get access to clinical participant via RelatedManager
        :param value:
        :return:
        """
        if value.first():
            participant = value.first().participant
        else:
            participant = 'None'
        return participant

    class Meta:
        model = SymptomsHallucination
        template_name = 'django_tables2/bootstrap.html'
        attrs = {"class": "ui-responsive table table-hover"}
        fields = ['participant', 'final_hallucinations', 'severe_hallucinations', 'auditory_hallucinations',
                  'auditory_commentary_hallucinations','visual_hallucinations', 'olf_gust_hallucinations',
                  'somatic_hallucinations']

class SymptomsBehaviourTable(tables.Table):
    participant = tables.LinkColumn('clinical_detail', verbose_name="Participant", accessor=A('clinical_behaviour'),
                                    args=[A('pk')])

    def render_participant(self, value):
        """
        Get access to clinical participant via RelatedManager
        :param value:
        :return:
        """
        if value.first():
            participant = value.first().participant
        else:
            participant = 'None'
        return participant

    class Meta:
        model = SymptomsBehaviour
        template_name = 'django_tables2/bootstrap.html'
        attrs = {"class": "ui-responsive table table-hover"}
        fields = ['participant', 'disorg_speech', 'severe_disorg_speech', 'disorg_catatonic_behav',
                  'severe_disorg_catatonic_behav','negative_symptoms', 'affective_flattening',
                  'allogia', 'avolition', 'anhedonia']

class SymptomsDepressionTable(tables.Table):
    participant = tables.LinkColumn('clinical_detail', verbose_name="Participant", accessor=A('clinical_depression'),
                                    args=[A('pk')])

    def render_participant(self, value):
        """
        Get access to clinical participant via RelatedManager
        :param value:
        :return:
        """
        if value.first():
            participant = value.first().participant
        else:
            participant = 'None'
        return participant

    class Meta:
        model = SymptomsDepression
        template_name = 'django_tables2/bootstrap.html'
        attrs = {"class": "ui-responsive table table-hover"}
        fields = ['participant', 'final_depression', 'depressed_mood', 'depression_anhedonia',
                  'app_wt_change', 'sleep_disturb', 'psych_change',
                  'fatigue_energyloss', 'worthless_guilt', 'decreased_conc', 'death_suicide',
                  'depressive_symptoms_count']

class SymptomsManiaTable(tables.Table):
    participant = tables.LinkColumn('clinical_detail', verbose_name="Participant", accessor=A('clinical_mania'),
                                    args=[A('pk')])

    def render_participant(self, value):
        """
        Get access to clinical participant via RelatedManager
        :param value:
        :return:
        """
        if value.first():
            participant = value.first().participant
        else:
            participant = 'None'
        return participant

    class Meta:
        model = SymptomsMania
        template_name = 'django_tables2/bootstrap.html'
        attrs = {"class": "ui-responsive table table-hover"}
        fields = ['participant', 'final_mania', 'elevated_mood', 'irritable_mood',
                  'grandiosity', 'decreased_sleep', 'pressured_speech',
                  'racing_thoughts', 'distractibility', 'psychmotor_agitation', 'risky_behaviour',
                  'manic_count']
