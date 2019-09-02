from django.http import HttpRequest
from django.test import TestCase, SimpleTestCase
from django.urls import reverse
import datetime

from szgenapp.models.studies import Study, STATUS_CHOICES
from szgenapp.models.participants import Participant, PARTICIPANT_STATUS_CHOICES, StudyParticipant, COUNTRY_CHOICES
from szgenapp.models.clinical import *
from szgenapp.forms.clinical import *


class ClinicalTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.study = Study.objects.create(title="TestStudy", precursor="T", description="My test study",
                                         status=STATUS_CHOICES[0])
        cls.participant = Participant.objects.create(alphacode="ABC",
                                                     country=COUNTRY_CHOICES[0],
                                                     secondaryid="ABC001",
                                                     status=PARTICIPANT_STATUS_CHOICES[0],
                                                     npid=1460001,
                                                     )
        cls.studyparticipant = StudyParticipant.objects.create(participant=cls.participant,
                                                               study=cls.study,
                                                               fullnumber='',
                                                               family='123',
                                                               individual='001')
        # Create subparts first
        cls.demo = Demographic.objects.create(gender='M', age_assessment=24, marital_status=1, living_arr=1,
                                              years_school=4, current_emp_status=1, employment_history=1)
        cls.diag = Diagnosis.objects.create(summary=1, age_onset=23, illness_duration=3, illness_duration_approx=False,
                                            age_first_treatment=10, dup=4, dup_approx=True, hospitalisation=1,
                                            hospitalisation_number=3, hospitalisation_number_approx=True)
        cls.medical = MedicalHistory.objects.create(thyroid=1, epilepsy=1, head_injury=1, abnormal_bed=1,
                                                    intellectual_disability=1, alcohol=1, cannabis=1,
                                                    other_drug='drug1', suicide=1, suicide_serious=1)
        cls.symptoms_general = SymptomsGeneral.objects.create(onset=1, severity_pattern=1, symptom_pattern=1,
                                                              illness_course=1, curr_gaf=1, wl_gaf=1,
                                                              current_ap_medication=1, clozapine_status=1,
                                                              treatment_resistant=1)
        cls.symptoms_delusion = SymptomsDelusion.objects.create(final_delusions=1, sevcur_delusions=1,
                                                                bizarre_delusions=1, biw_delusions=1,
                                                                control_delusions=1, persecutory_delusions=1,
                                                                reference_delusions=1, jealousy_delusions=1,
                                                                guilt_sin_delusions=1, grandiose_delusions=1,
                                                                religious_delusions=1, somatic_delusions=1,
                                                                eroto_delusions=1, mindread_delusions=1)
        cls.symptoms_hallucination = SymptomsHallucination.objects.create(final_hallucinations=1,
                                                                          severe_hallucinations=1,
                                                                          auditory_hallucinations=1,
                                                                          auditory_commentary_hallucinations=1,
                                                                          visual_hallucinations=1,
                                                                          olf_gust_hallucinations=1,
                                                                          somatic_hallucinations=1)
        cls.symptoms_behaviour = SymptomsBehaviour.objects.create(disorg_speech=1,severe_disorg_speech=1,
                                                                  disorg_catatonic_behav=1,
                                                                  severe_disorg_catatonic_behav=1,
                                                                  negative_symptoms=1,
                                                                  affective_flattening=1,
                                                                  allogia=1,
                                                                  avolition=1,
                                                                  anhedonia=1)
        cls.symptoms_depression = SymptomsDepression.objects.create(final_depression=1, depressed_mood=1,
                                                                    depression_anhedonia=1,
                                                                    app_wt_change=1,
                                                                    sleep_disturb=1,
                                                                    psych_change=1,
                                                                    fatigue_energyloss=1,
                                                                    worthless_guilt=1,
                                                                    decreased_conc=1,
                                                                    death_suicide=1,
                                                                    depressive_symptoms_count=4)
        cls.symptoms_mania = SymptomsMania.objects.create(final_mania=1, elevated_mood=1,
                                                          irritable_mood=1, grandiosity=1,
                                                          decreased_sleep=1, pressured_speech=1,
                                                          racing_thoughts=1, distractibility=1,
                                                          psychmotor_agitation=1, risky_behaviour=1,
                                                          manic_count=4)

        # Create clinical record with all foreign keys
        cls.clin1 = Clinical.objects.create(participant=cls.studyparticipant,
                                            demographic=cls.demo,
                                            diagnosis=cls.diag,
                                            medical=cls.medical,
                                            symptoms_general=cls.symptoms_general,
                                            symptoms_delusion=cls.symptoms_delusion,
                                            symptoms_hallucination=cls.symptoms_hallucination,
                                            symptoms_behaviour=cls.symptoms_behaviour,
                                            symptoms_depression=cls.symptoms_depression,
                                            symptoms_mania=cls.symptoms_mania
                                            )
        # < QueryDict: {'csrfmiddlewaretoken': ['ISXGN6JXUL1Nng66fWFJhopkFQ5tBNqqQThepDVgUOrWUwMfs02PD5WFnP1qReYg'],
        #               'participant': ['2'], '_submit': [''], 'gender': ['F'], 'age_assessment': ['48'],
        #               'marital_status': ['nevmar'], 'living_arr': ['facility'], 'years_school': ['10'],
        #               'current_emp_status': ['never worked'], 'employment_history': ['5'], 'summary': ['SZ'],
        #               'age_onset': ['18'], 'illness_duration': ['30'], 'age_first_treatment': ['18'], 'dup': ['0'],
        #               'hospitalisation': ['Yes'], 'hospitalisation_number': ['11'], 'thyroid': ['No'],
        #               'epilepsy': ['No'], 'head_injury': ['No'], 'abnormal_bed': ['No'],
        #               'intellectual_disability': ['No'], 'alcohol': ['No'], 'cannabis': ['No'], 'other_drug': ['No'],
        #               'other_drug_type': [''], 'suicide': ['Yes'], 'suicide_serious': ['Yes'], 'onset': ['ABRUPT'],
        #               'severity_pattern': ['1'], 'symptom_pattern': ['1'], 'illness_course': ['1'],
        #               'curr_gaf': ['None'], 'wl_gaf': ['Moderate'], 'current_ap_medication': ['Yes'],
        #               'clozapine_status': ['Yes'], 'treatment_resistant': ['Yes'], 'final_delusions': ['Yes'],
        #               'sevcur_delusions': ['Question'], 'bizarre_delusions': ['No'], 'biw_delusions': ['No'],
        #               'control_delusions': ['Yes'], 'persecutory_delusions': ['Yes'], 'reference_delusions': ['Yes'],
        #               'jealousy_delusions': ['Yes'], 'guilt_sin_delusions': ['Yes'], 'grandiose_delusions': ['Yes'],
        #               'religious_delusions': ['NO'], 'somatic_delusions': ['Yes'], 'eroto_delusions': ['Yes'],
        #               'mindread_delusions': ['No'], 'final_depression': ['Yes'], 'depressed_mood': ['Yes'],
        #               'depression_anhedonia': ['Yes'], 'app_wt_change': ['Yes'], 'sleep_disturb': ['No'],
        #               'psych_change': ['Yes'], 'fatigue_energyloss': ['Yes'], 'worthless_guilt': ['Yes'],
        #               'decreased_conc': ['No'], 'death_suicide': ['Yes'], 'depressive_symptoms_count': ['4'],
        #               'final_hallucinations': ['Yes'], 'severe_hallucinations': ['Mild'],
        #               'auditory_hallucinations': ['Yes'], 'auditory_commentary_hallucinations': ['Yes'],
        #               'visual_hallucinations': ['No'], 'olf_gust_hallucinations': ['Yes'],
        #               'somatic_hallucinations': ['Yes'], 'disorg_speech': ['Yes'], 'severe_disorg_speech': ['Question'],
        #               'disorg_catatonic_behav': ['Yes'], 'severe_disorg_catatonic_behav': ['Question'],
        #               'negative_symptoms': ['Yes'], 'affective_flattening': ['Severe'], 'allogia': ['Severe'],
        #               'avolition': ['Marked'], 'anhedonia': ['Marked'], 'final_mania': ['Yes'],
        #               'elevated_mood': ['Yes'], 'irritable_mood': ['Yes'], 'grandiosity': ['Yes'],
        #               'decreased_sleep': ['Yes'], 'pressured_speech': ['No'], 'racing_thoughts': ['Yes'],
        #               'distractibility': ['Yes'], 'psychmotor_agitation': ['Yes'], 'risky_behaviour': ['Yes'],
        #               'manic_count': ['5']} >

    def test_home_page_status_code(self):
        response = self.client.get('/clinical/')
        self.assertEquals(response.status_code, 200)

    def test_view_url_by_name(self):
        response = self.client.get(reverse('clinical_list'))
        self.assertEquals(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('clinical_list'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'clinical/clinical-list.html')

    def test_home_page_contains_correct_html(self):
        response = self.client.get('/clinical/')
        self.assertContains(response, '<h2>Clinical Records:')

    def test_home_page_does_not_contain_incorrect_html(self):
        response = self.client.get('/clinical/')
        self.assertNotContains(
            response, 'Welcome to the SZGEN Database')

    def test_clinical_participant_set(self):
        self.assertEqual(self.clin1.participant, self.studyparticipant)

    def test_clinical_demographic_set(self):
        self.assertEqual(self.clin1.demographic, self.demo)
        self.assertEqual(self.demo.gender, 'M')
        self.assertEqual(self.clin1.demographic.gender, 'M')

    def test_clinical_diagnosis_set(self):
        self.assertEqual(self.clin1.diagnosis, self.diag)
        self.assertEqual(self.diag.age_onset, 23)
        self.assertEqual(self.clin1.diagnosis.age_onset, 23)

    def test_clinical_diagnosis_boolean_true(self):
        self.assertNotEqual(self.clin1.diagnosis.dup_approx, 'true')
        self.assertEqual(self.clin1.diagnosis.dup_approx, True)
        self.assertEqual(self.clin1.diagnosis.dup_approx, 1)

    def test_clinical_diagnosis_boolean_false(self):
        self.assertNotEqual(self.clin1.diagnosis.illness_duration_approx, 'false')
        self.assertEqual(self.clin1.diagnosis.illness_duration_approx, False)
        self.assertEqual(self.clin1.diagnosis.illness_duration_approx, 0)

    def test_clinical_diagnosis_form(self):
        form = DiagnosisForm()
        self.assertFalse(form.is_valid(), 'Empty form is invalid')
        testform = DiagnosisForm(
            {'summary': 'SAD', 'age_onset': 23, 'illness_duration': 1, 'illness_duration_approx': True,
             'age_first_treatment': 34, 'dup': 34, 'dup_approx': False, 'hospitalisation': 'Yes',
             'hospitalisation_number': 2, 'hospitalisation_number_approx': False})
        self.assertTrue(testform.is_valid(), 'Full form is valid')
        self.assertFalse(testform.cleaned_data['hospitalisation_number_approx'], 'Boolean field set to False')
        self.assertTrue(testform.cleaned_data['illness_duration_approx'], 'Boolean field set to True')

