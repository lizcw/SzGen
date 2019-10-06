from django.db import models

from szgenapp.validators import validate_age, validate_school_years, validate_onset_age, validate_ill_duration, \
    validate_number_hosp, validate_manic_count, validate_depression_count

GENDER_CHOICES = (
    ('M', 'Male'),
    ('F', 'Female'),
    ('O', 'Other')
)

BOOLEAN_CHOICES = (
    ('Yes', 'Yes'),
    ('No', 'No'),
    ('Unk', 'Unknown')
)

MARITAL_STATUS_CHOICES = (
    ('married', 'Married'),
    ('nevmar', 'Single or Never married'),
    ('sepdiv', 'Separated or divorced'),
    ('widowed', 'Widowed, not remarried'),
    ('unknown', 'Unknown')
)

LIVING_CHOICES = (
    ('alone', 'Lives alone (including hostel)'),
    ('facility', 'Lives in a psychiatric treatment facility'),
    ('family', 'Lives with biological family members and/or spouse'),
    ('others', 'Lives with people who are not family (e.g. friends, housemates)'),
    ('unknown', 'Unknown')
)

EMPLOYMENT_CHOICES = (
    ('disabled', 'Formerly worked, no longer able (disabled)'),
    ('homemaker', 'Homemaker primary role'),
    ('never worked', 'Never worked at least 30% of time'),
    ('student', 'Full-time student'),
    ('unemployed', 'Not disabled but not working (unemployed)'),
    ('working', 'Working at least 30% of time'),
    ('unknown', 'Unknown')
)

EMPLOYMENT_HISTORY_CHOICES = (
    (1, 'Always worked'),
    (2, 'Periods of unemployment not related to illness'),
    (3, 'Minor occupational dysfunction'),
    (4, 'Moderate occupational dysfunction'),
    (5, 'Severe occupational dysfunction'),
    (0, 'Unknown')

)

DSMIV_CHOICES = (
    ('SAD', 'Schizoaffective, depressed'),
    ('SAM', 'Schizoaffective, bipolar'),
    ('SZ', 'Schizophrenia')
)

SEVERITY_CHOICES = (
    ('Nil', 'None'),  # 'Nil' REQUIRED TO PREVENT PYTHON 'None' TYPE MATCH
    ('Question', 'Question'),
    ('Mild', 'Mild'),
    ('Moderate', 'Moderate'),
    ('Marked', 'Marked'),
    ('Severe', 'Severe'),
    ('Unknown', 'Unknown')
)

SEVERITY_PATTERN_CHOICES = (
    (1, 'Episodic shift (no deterioration when not actively unwell)'),
    (2, 'Mild deterioration'),
    (3, 'Moderate deterioration'),
    (4, 'Severe deterioration'),
    (0, 'Unknown')
)

SYMPTOM_PATTERN_CHOICES = (
    (1, 'Continuously positive'),
    (2, 'Predominantly negative'),
    (3, 'Positive converting to negative'),
    (4, 'Negative converting to positive (0 observations coded "4")'),
    (5, 'Continuous mixture of positive and negative symptoms'),
    (0, 'Unknown')
)
RELIGIOUS_CHOICES = (
    ('No', 'No'),
    ('Yes', 'Yes'),
    ('Cul', 'Culturally acceptable (non-delusional) beliefs'),
    ('Unk', 'Unknown')
)

ONSET_CHOICES = (
    ('Abrupt', 'Abrupt (within a day)'),
    ('Acute', 'Acute (within a week)'),
    ('ModAcute', 'Moderately acute (within a month)'),
    ('Gradual', 'Gradual (longer than a month)'),
    ('Unknown', 'Unknown')
)

ILLNESS_CHOICES = (
    (1, 'Episodic with interepisode residual symptoms'),
    (2, 'Episodic with no interepisode residual symptoms'),
    (3, 'Continuous'),
    (4, 'Single episode in partial remission'),
    (5, 'Single episode in full remission'),
    (6, 'Other, unspecified, unknown course')
)

GAF_CHOICES = (
    ('Nil', '81-100 (None)'),  # 'Nil' REQUIRED TO PREVENT PYTHON 'None' TYPE MATCH
    ('Mild', '61-80 (Mild)'),
    ('Moderate', '31-60 (Moderate)'),
    ('Severe', '1-30 (Severe)'),
    ('Unknown', 'Unknown')
)

WL_GAF_CHOICES = (
    ('Mild', '61-80 (Mild)'),
    ('Moderate', '31-60 (Moderate)'),
    ('Severe', '1-30 (Severe)'),
    ('Unknown', 'Unknown')
)

CLINICAL_SUBSETS = ['demographic', 'diagnosis', 'medical', 'symptoms_general', 'symptoms_delusion',
                    'symptoms_hallucination', 'symptoms_behaviour', 'symptoms_depression', 'symptoms_mania']
CLINICAL_SUBTABLES = ['demographic', 'diagnosis', 'medicalhistory', 'symptomsgeneral', 'symptomsdelusion',
                      'symptomshallucination', 'symptomsbehaviour', 'symptomsdepression', 'symptomsmania']


### Admin managed lookup lists
class Gender(models.Model):
    code = models.CharField(primary_key=True, max_length=3, blank=False, null=False, help_text='Gender code')
    name = models.CharField(max_length=30, blank=False, null=False, help_text='Gender name')

    class Meta:
        verbose_name = 'Gender'
        verbose_name_plural = 'Genders'

    def __str__(self):
        return '%s' % self.name


class MaritalStatus(models.Model):
    code = models.CharField(primary_key=True, max_length=30, help_text='Marital Status code')
    name = models.CharField(max_length=100, blank=False, null=False, help_text='Marital Status name')

    class Meta:
        verbose_name = 'Marital Status'
        verbose_name_plural = 'Marital Statuses'

    def __str__(self):
        return '%s' % self.name


class Living(models.Model):
    code = models.CharField(primary_key=True, max_length=30, help_text='Living code')
    name = models.CharField(max_length=100, blank=False, null=False, help_text='Living name')

    class Meta:
        verbose_name = 'Living'
        verbose_name_plural = 'Living options'

    def __str__(self):
        return '%s' % self.name


class Employment(models.Model):
    code = models.CharField(primary_key=True, max_length=30, help_text='Employment code')
    name = models.CharField(max_length=100, blank=False, null=False, help_text='Employment name')

    class Meta:
        verbose_name = 'Employment'
        verbose_name_plural = 'Employment options'

    def __str__(self):
        return '%s' % self.name


class EmploymentHistory(models.Model):
    code = models.SmallIntegerField(primary_key=True, help_text='Employment History code')
    name = models.CharField(max_length=100, blank=False, null=False, help_text='Employment History name')

    class Meta:
        verbose_name = 'Employment History'
        verbose_name_plural = 'Employment History options'

    def __str__(self):
        return '%s' % self.name


class Dsmiv(models.Model):
    code = models.CharField(primary_key=True, max_length=5, help_text='DSMIV code')
    name = models.CharField(max_length=30, blank=False, null=False, help_text='DSMIV name')

    class Meta:
        verbose_name = 'DSMIV'
        verbose_name_plural = 'DSMIV options'

    def __str__(self):
        return '%s' % self.name


class Severity(models.Model):
    code = models.CharField(primary_key=True, max_length=20, help_text='Severity code')
    name = models.CharField(max_length=50, blank=False, null=False, help_text='Severity name')

    class Meta:
        verbose_name = 'Severity'
        verbose_name_plural = 'Severity options'

    def __str__(self):
        return '%s' % self.name


class SeverityPattern(models.Model):
    code = models.SmallIntegerField(primary_key=True, help_text='Severity Pattern code')
    name = models.CharField(max_length=100, blank=False, null=False, help_text='Severity Pattern name')

    class Meta:
        verbose_name = 'Severity Pattern'
        verbose_name_plural = 'Severity Pattern options'

    def __str__(self):
        return '%s' % self.name


class SymptomPattern(models.Model):
    code = models.SmallIntegerField(primary_key=True, help_text='Symptom Pattern code')
    name = models.CharField(max_length=100, blank=False, null=False, help_text='Symptom Pattern name')

    class Meta:
        verbose_name = 'Symptom Pattern'
        verbose_name_plural = 'Symptom Pattern options'

    def __str__(self):
        return '%s' % self.name


class Religious(models.Model):
    code = models.CharField(primary_key=True, max_length=10, help_text='Religious code')
    name = models.CharField(max_length=100, blank=False, null=False, help_text='Religious name')

    class Meta:
        verbose_name = 'Religious'
        verbose_name_plural = 'Religious options'

    def __str__(self):
        return '%s' % self.name


class Onset(models.Model):
    code = models.CharField(primary_key=True, max_length=20, help_text='Onset code')
    name = models.CharField(max_length=100, blank=False, null=False, help_text='Onset name')

    class Meta:
        verbose_name = 'Onset'
        verbose_name_plural = 'Onset options'

    def __str__(self):
        return '%s' % self.name


class Illness(models.Model):
    code = models.SmallIntegerField(primary_key=True, help_text='Illness code')
    name = models.CharField(max_length=100, blank=False, null=False, help_text='Illness name')

    class Meta:
        verbose_name = 'Illness'
        verbose_name_plural = 'Illness options'

    def __str__(self):
        return '%s' % self.name


class Gaf(models.Model):
    code = models.CharField(primary_key=True, max_length=20, help_text='GAF code')
    name = models.CharField(max_length=100, blank=False, null=False, help_text='GAF name')

    class Meta:
        verbose_name = 'GAF'
        verbose_name_plural = 'GAF options'

    def __str__(self):
        return '%s' % self.name


class Gafwl(models.Model):
    code = models.CharField(primary_key=True, max_length=20, help_text='WL GAF code')
    name = models.CharField(max_length=100, blank=False, null=False, help_text='WL GAF name')

    class Meta:
        verbose_name = 'WL GAF'
        verbose_name_plural = 'WL GAF options'

    def __str__(self):
        return '%s' % self.name


############################################################
# Clinical models
class Clinical(models.Model):
    """
    Clinical data per participant - subsectioned
    """
    id = models.AutoField(primary_key=True)
    participant = models.ForeignKey('StudyParticipant', on_delete=models.CASCADE, related_name='clinical')

    def __str__(self):
        return 'Clinical record for %s' % self.participant.getFullNumber()

    def get_sub_fields(self, category):
        """
        Returns dict of subcategory field labels and values
        :return: dict(label, value)
        """
        display_fields = []
        parent = self
        if category == 'demographic':
            parent = self.demographic
        elif category == 'diagnosis':
            parent = self.diagnosis
        elif category == 'medical':
            parent = self.medicalhistory
        elif category == 'symptoms_general':
            parent = self.symptomsgeneral
        elif category == 'symptoms_delusion':
            parent = self.symptomsdelusion
        elif category == 'symptoms_hallucination':
            parent = self.symptomshallucination
        elif category == 'symptoms_behaviour':
            parent = self.symptomsbehaviour
        elif category == 'symptoms_depression':
            parent = self.symptomsdepression
        elif category == 'symptoms_mania':
            parent = self.symptomsmania

        values = parent._meta.fields
        if len(values) > 0:
            for field in values:
                get_choice = 'get_' + field.name + '_display'
                if hasattr(parent, get_choice):
                    value = getattr(parent, get_choice)()
                else:
                    try:
                        value = getattr(parent, field.name)
                    except AttributeError:
                        value = None

                display_fields.append(
                    {
                        'label': field.verbose_name,
                        'name': field.name,
                        'value': value,
                    }
                )
        return display_fields

    def get_demographic_fields(self):
        return self.get_sub_fields('demographic')

    def get_diagnosis_fields(self):
        return self.get_sub_fields('diagnosis')

    def get_medical_fields(self):
        return self.get_sub_fields('medical')

    def get_symptoms_general_fields(self):
        return self.get_sub_fields('symptoms_general')

    def get_symptoms_delusion_fields(self):
        return self.get_sub_fields('symptoms_delusion')

    def get_symptoms_hallucination_fields(self):
        return self.get_sub_fields('symptoms_hallucination')

    def get_symptoms_behaviour_fields(self):
        return self.get_sub_fields('symptoms_behaviour')

    def get_symptoms_depression_fields(self):
        return self.get_sub_fields('symptoms_depression')

    def get_symptoms_mania_fields(self):
        return self.get_sub_fields('symptoms_mania')


class Demographic(models.Model):
    """
    Clinically recorded demographic data
    """
    clinical = models.OneToOneField(Clinical, on_delete=models.CASCADE, primary_key=True)
    gender = models.ForeignKey(Gender, on_delete=models.SET_NULL, null=True, blank=True,
                               help_text='Gender of participant')
    age_assessment = models.IntegerField(verbose_name='Age', validators=[validate_age],
                                         help_text='Age at the time of assessment', null=True, blank=True)
    marital_status = models.ForeignKey(MaritalStatus, on_delete=models.SET_NULL, null=True, blank=True,
                                       help_text='Marital status at the time of assessment')
    living_arr = models.ForeignKey(Living, on_delete=models.SET_NULL, null=True, blank=True,
                                   verbose_name='Living arrangement',
                                   help_text='Who the individual currently resides with (at time of assessment)'
                                   )
    years_school = models.IntegerField(validators=[validate_school_years], help_text='Years of formal schooling',
                                       null=True, blank=True)
    current_emp_status = models.ForeignKey(Employment, on_delete=models.SET_NULL, null=True, blank=True,
                                           verbose_name='Current Employment',
                                           help_text='Employment status (at time of assessment)')
    employment_history = models.ForeignKey(EmploymentHistory, on_delete=models.SET_NULL, null=True, blank=True,
                                           verbose_name='Past Employment',
                                           help_text='Level of occupational disability over the past 5 years'
                                           )


class Diagnosis(models.Model):
    """
    Clinically recorded diagnosis
    """
    clinical = models.OneToOneField(Clinical, on_delete=models.CASCADE, primary_key=True)
    summary = models.ForeignKey(Dsmiv, on_delete=models.SET_NULL, null=True, blank=True,
                                verbose_name='DSMIV', help_text='DSMIV Diagnosis')
    age_onset = models.IntegerField(help_text='Age at onset of psychosis', validators=[validate_onset_age], null=True,
                                    blank=True)
    illness_duration = models.IntegerField(help_text='Illness duration (onset to current) in years',
                                           validators=[validate_ill_duration], null=True, blank=True)
    illness_duration_approx = models.BooleanField(default=False,
                                                  verbose_name='Illness duration is approximate',
                                                  help_text='Period for illness duration is approximate (eg 20+)')
    age_first_treatment = models.IntegerField(help_text='Age at which psychiatric treatment first accessed',
                                              validators=[validate_onset_age], null=True, blank=True)
    dup = models.IntegerField(verbose_name='DUP',
                              help_text='Duration of Untreated Psychosis (DUP): Period between onset and first treatment (in years)',
                              null=True, blank=True)
    dup_approx = models.BooleanField(default=False,
                                     verbose_name="DUP is approximate",
                                     help_text='Period for DUP is approximate (eg 20+)')
    hospitalisation = models.CharField(max_length=10, choices=BOOLEAN_CHOICES, null=True, blank=True,
                                       help_text='Whether the individual has ever been hospitalised for psychiatric reasons')
    hospitalisation_number = models.IntegerField(verbose_name='Number of hospitalisations', null=True, blank=True,
                                                 help_text='Number of psychiatric hospitalisations (lifetime)',
                                                 validators=[validate_number_hosp])
    hospitalisation_number_approx = models.BooleanField(default=False,
                                                        verbose_name="Number of hospitalisations is approximate",
                                                        help_text='Number of hospitalisations is approximate (eg >5)')

    def __str__(self):
        return self.summary


class MedicalHistory(models.Model):
    """
    Clinically recorded Medical History
    """
    clinical = models.OneToOneField(Clinical, on_delete=models.CASCADE, primary_key=True)
    thyroid = models.CharField(max_length=10, choices=BOOLEAN_CHOICES, null=True, blank=True, verbose_name='Thyroid',
                               help_text='Definite evidence of clinically significant thyroid problems')
    epilepsy = models.CharField(max_length=10, choices=BOOLEAN_CHOICES, null=True, blank=True, verbose_name='Epilepsy',
                                help_text='Definite evidence of epilepsy or clinically significant seizures')
    head_injury = models.CharField(max_length=10, choices=BOOLEAN_CHOICES, null=True, blank=True,
                                   verbose_name='Head Injury',
                                   help_text='Definite evidence of a significant head injury (i.e.  '
                                             'serious enough to involve loss of consciousness) (lifetime)')
    abnormal_bed = models.CharField(max_length=10, choices=BOOLEAN_CHOICES, null=True, blank=True,
                                    verbose_name='Abnormal birth or early development',
                                    help_text="Definite evidence of clinically significant birth complications "
                                              "during individual's birth, or definite delayed developmental "
                                              "milestones")
    intellectual_disability = models.CharField(max_length=10, choices=BOOLEAN_CHOICES, null=True, blank=True,
                                               verbose_name='Intellectual disability',
                                               help_text='Intelluctual disability: IQ assessed <75')
    alcohol = models.CharField(max_length=10, choices=BOOLEAN_CHOICES, null=True, blank=True,
                               verbose_name='Alcohol Use Disorder',
                               help_text='DSMIV lifetime alcohol abuse and/or dependence')
    cannabis = models.CharField(max_length=10, choices=BOOLEAN_CHOICES, null=True, blank=True,
                                verbose_name='Cannabis Use Disorder',
                                help_text='DSMIV lifetime cannabis abuse and/or dependence')
    other_drug = models.CharField(max_length=10, choices=BOOLEAN_CHOICES, null=True, blank=True,
                                  verbose_name='Other Drug Use Disorder',
                                  help_text='DSMIV lifetime other illicit drug abuse and/or dependence')
    other_drug_type = models.TextField(null=True, blank=True, verbose_name='Illicit Drug Use Disorder Type',
                                       help_text="Types of illicit drugs for which the individual meets the DSMIV "
                                                 "criteria for lifetime abuse and/or dependence. "
                                                 "Blank for all individuals where OthDrug is not 'Yes'")
    suicide = models.CharField(max_length=10, choices=BOOLEAN_CHOICES, null=True, blank=True,
                               verbose_name='Suicide Attempts',
                               help_text='Whether the individual has ever attempted suicide')
    suicide_serious = models.CharField(max_length=10, choices=BOOLEAN_CHOICES, null=True, blank=True,
                                       verbose_name='Serious Suicidal Intent',
                                       help_text='Whether the individual\'s most serious/severe suicide attempt '
                                                 'involved serious intent to die.')


"""
    Symptoms subcategorized into:
    1. General
    2. Delusions
    3. Hallucinations
    4. Behaviour
    5. Depression
    6. Mania
    """


class SymptomsGeneral(models.Model):
    """
    1. General
    """
    clinical = models.OneToOneField(Clinical, on_delete=models.CASCADE, primary_key=True)
    onset = models.ForeignKey(Onset, on_delete=models.SET_NULL, null=True, blank=True,
                             verbose_name='Onset of Psychosis',
                             help_text='Rapidity of prodromal period (between noticeable social/occupational decline '
                                       'and definite onset of psychosis)')
    severity_pattern = models.ForeignKey(SeverityPattern, on_delete=models.SET_NULL, null=True, blank=True,
                                                verbose_name='Severity Pattern',
                                                help_text='Pattern of severity of decline in functioning over the course '
                                                          'of the illness, as defined in the DIGS')
    symptom_pattern = models.ForeignKey(SymptomPattern, on_delete=models.SET_NULL, null=True, blank=True,
                                               verbose_name='Symptom Pattern',
                                               help_text='Relationship between positive and negative symptoms throughout '
                                                         'the course of the illness, as defined in the DIGS')
    illness_course = models.ForeignKey(Illness, on_delete=models.SET_NULL, null=True, blank=True,
                                              verbose_name='Illness Course',
                                              help_text='Categorical illness course, as defined in the DIGS')
    curr_gaf = models.ForeignKey(Gaf, on_delete=models.SET_NULL, null=True, blank=True,
                                verbose_name='Current Global Assessment of Function (GAF)',
                                help_text='Current (past 30 days) rating on the Global Assessment of Function Scale')
    wl_gaf = models.ForeignKey(Gafwl, on_delete=models.SET_NULL, null=True, blank=True,
                              verbose_name='Worst Lifetime Global Assessment of Function (GAF)',
                              help_text='Lowest (lifetime) rating on the Global Assessment of Function Scale')
    current_ap_medication = models.CharField(max_length=10, choices=BOOLEAN_CHOICES, null=True, blank=True,
                                             verbose_name='Current Antipsychotic medication',
                                             help_text='Whether the individual is definitely taking antipsychotic '
                                                       'medication at the time of assessment')
    clozapine_status = models.CharField(max_length=10, choices=BOOLEAN_CHOICES, null=True, blank=True,
                                        verbose_name='Clozapine Status',
                                        help_text='Whether the individual is definitely taking clozapine at the '
                                                  'time of assessment (Mandatory)')
    treatment_resistant = models.CharField(max_length=10, choices=BOOLEAN_CHOICES, null=True, blank=True,
                                           verbose_name='Treatment Resistant',
                                           help_text='Whether the individual meets strictly defined criteria for '
                                                     'treatment resistance (Mandatory)')


class SymptomsDelusion(models.Model):
    """
    2. Delusions
    """
    clinical = models.OneToOneField(Clinical, on_delete=models.CASCADE, primary_key=True)
    final_delusions = models.CharField(max_length=10, choices=BOOLEAN_CHOICES, null=True, blank=True,
                                       verbose_name='Final Delusions',
                                       help_text='Definite (lifetime) presence of delusions')
    sevcur_delusions = models.ForeignKey(Severity, on_delete=models.SET_NULL, null=True, blank=True,
                                         related_name='sevcur_delusions',
                                        verbose_name='Severity of Current Delusions',
                                        help_text='Severity of current delusions (past 30 days)')
    bizarre_delusions = models.CharField(max_length=10, choices=BOOLEAN_CHOICES, null=True, blank=True,
                                         verbose_name='Bizarre Delusions',
                                         help_text='Presence (lifetime) of definitely bizarre delusions')
    biw_delusions = models.CharField(max_length=10, choices=BOOLEAN_CHOICES, null=True, blank=True,
                                     verbose_name='Broadcast / Insertion / Withdrawal Delusions',
                                     help_text='Presence (lifetime) of thought broadcast/insertion/withdrawal'
                                               ' delusions')
    control_delusions = models.CharField(max_length=10, choices=BOOLEAN_CHOICES, null=True, blank=True,
                                         verbose_name='Control Delusions',
                                         help_text='Presence (lifetime) of delusions of control of thought or '
                                                   'actions')
    persecutory_delusions = models.CharField(max_length=10, choices=BOOLEAN_CHOICES, null=True, blank=True,
                                             verbose_name='Persecutory Delusions',
                                             help_text='Presence (lifetime) of persecutory delusions')
    reference_delusions = models.CharField(max_length=10, choices=BOOLEAN_CHOICES, null=True, blank=True,
                                           verbose_name='Referential Delusions',
                                           help_text='Presence (lifetime) of delusions of reference')
    jealousy_delusions = models.CharField(max_length=10, choices=BOOLEAN_CHOICES, null=True, blank=True,
                                          verbose_name='Jealousy Delusions',
                                          help_text='Presence (lifetime) of delusions of jealousy')
    guilt_sin_delusions = models.CharField(max_length=10, choices=BOOLEAN_CHOICES, null=True, blank=True,
                                           verbose_name='Guilt / Sin Delusions',
                                           help_text='Presence (lifetime) of guilt or sin delusions')
    grandiose_delusions = models.CharField(max_length=10, choices=BOOLEAN_CHOICES, null=True, blank=True,
                                           verbose_name='Grandiose Delusions',
                                           help_text='Presence (lifetime) of grandiose delusions')
    religious_delusions = models.ForeignKey(Religious, on_delete=models.SET_NULL, null=True, blank=True,
                                           verbose_name='Religious / Magic Delusions',
                                           help_text='Presence (lifetime) of religious delusions or delusions of magic')
    somatic_delusions = models.CharField(max_length=10, choices=BOOLEAN_CHOICES, null=True, blank=True,
                                         verbose_name='Somatic Delusions',
                                         help_text='Presence (lifetime) of somatic delusions')
    eroto_delusions = models.CharField(max_length=10, choices=BOOLEAN_CHOICES, null=True, blank=True,
                                       verbose_name='Erotomanic Delusions',
                                       help_text='Presence (lifetime) of erotomanic delusions')
    mindread_delusions = models.CharField(max_length=10, choices=BOOLEAN_CHOICES, null=True, blank=True,
                                          verbose_name='Mind Reading Delusions',
                                          help_text="Presence (lifetime) of delusions of mind reading (of "
                                                    "individual's mind by others)")


class SymptomsHallucination(models.Model):
    """
    3. Hallucination
    """
    clinical = models.OneToOneField(Clinical, on_delete=models.CASCADE, primary_key=True)
    final_hallucinations = models.CharField(max_length=10, choices=BOOLEAN_CHOICES, null=True, blank=True,
                                            verbose_name='Final Hallucinations',
                                            help_text='Definite (lifetime) presence of hallucinations')
    severe_hallucinations = models.ForeignKey(Severity, on_delete=models.SET_NULL, null=True, blank=True,
                                             verbose_name='Severity of Current Hallucinations',
                                             help_text="Severity of current hallucinations (past 30 days). "
                                                       "'Question' category usually grouped with "
                                                       "'Unknown' category for analyses")
    auditory_hallucinations = models.CharField(max_length=10, choices=BOOLEAN_CHOICES, null=True, blank=True,
                                               verbose_name='Auditory hallucinations',
                                               help_text='Presence (lifetime) of auditory hallucinations')
    auditory_commentary_hallucinations = models.CharField(max_length=10, choices=BOOLEAN_CHOICES, null=True, blank=True,
                                                          verbose_name='Commentary / 3rd Person Auditory '
                                                                       'Hallucinations',
                                                          help_text='Presence (lifetime) of auditory '
                                                                    'hallucinations involving commentary or '
                                                                    'third person conversations between voices')
    visual_hallucinations = models.CharField(max_length=10, choices=BOOLEAN_CHOICES, null=True, blank=True,
                                             verbose_name='Visual Hallucinations',
                                             help_text='Presence (lifetime) of visual hallucinations')
    olf_gust_hallucinations = models.CharField(max_length=10, choices=BOOLEAN_CHOICES, null=True, blank=True,
                                               verbose_name='Olfactory / Gustatory Hallucinations',
                                               help_text='Presence (lifetime) of olfactory or gustatory '
                                                         'hallucinations')
    somatic_hallucinations = models.CharField(max_length=10, choices=BOOLEAN_CHOICES, null=True, blank=True,
                                              verbose_name='Somatic / Tactile Hallucinations',
                                              help_text='Presence (lifetime) of somatic/tactile hallucinations')


class SymptomsBehaviour(models.Model):
    """
    4. Behaviour
    """
    clinical = models.OneToOneField(Clinical, on_delete=models.CASCADE, primary_key=True)
    disorg_speech = models.CharField(max_length=10, choices=BOOLEAN_CHOICES, null=True, blank=True,
                                     verbose_name='Disorganised Speech',
                                     help_text='Definite (lifetime) presence of disorganised speech/positive '
                                               'formal thought disorder')
    severe_disorg_speech = models.ForeignKey(Severity, on_delete=models.SET_NULL, null=True, blank=True,
                                             related_name='severe_disorg_speech',
                                            verbose_name='Severity of Current Disorganised Speech',
                                            help_text="Severity of current disorganised speech/positive formal "
                                                      "thought disorder (past 30 days). 'Question' category usually "
                                                      "grouped with 'Unknown' category for analyses")
    disorg_catatonic_behav = models.CharField(max_length=10, choices=BOOLEAN_CHOICES, null=True, blank=True,
                                              verbose_name='Disorganised / Catatonic Behaviour',
                                              help_text='Definite (lifetime) presence of disorganised/catatonic '
                                                        'behaviour')
    severe_disorg_catatonic_behav = models.ForeignKey(Severity, on_delete=models.SET_NULL, null=True, blank=True,
                                                      related_name='severe_disorg_catatonic_behav',
                                                     verbose_name='Severity of Current Disorganised Behaviour',
                                                     help_text='Severity of current disorganised/catatonic '
                                                               'behaviour (past 30 days)')
    negative_symptoms = models.CharField(max_length=10, choices=BOOLEAN_CHOICES, null=True, blank=True,
                                         verbose_name='Negative Symptoms',
                                         help_text='Definite (lifetime) presence of negative symptoms')
    affective_flattening = models.ForeignKey(Severity, on_delete=models.SET_NULL, null=True, blank=True,
                                             related_name='affective_flattening',
                                            verbose_name='Affective Flattening',
                                            help_text='Severity of current affective flattening/inappropriate '
                                                      'affect (past 30 days)')
    allogia = models.ForeignKey(Severity, on_delete=models.SET_NULL, null=True, blank=True,
                                related_name='allogia',
                                verbose_name='Alogia',
                               help_text='Severity of current alogia/negative thought disorder (past 30 days)')
    avolition = models.ForeignKey(Severity, on_delete=models.SET_NULL, null=True, blank=True,
                                  related_name='avolition',
                                 verbose_name='Avolition / Apathy',
                                 help_text='Severity of current avolition/apathy (past 30 days)')
    anhedonia = models.ForeignKey(Severity, on_delete=models.SET_NULL, null=True, blank=True,
                                  related_name='anhedonia',
                                 verbose_name='Anhedonia / Asociality',
                                 help_text='Severity of current anhedonia/asociality (past 30 days)')


class SymptomsDepression(models.Model):
    """
    5. Depression
    """
    clinical = models.OneToOneField(Clinical, on_delete=models.CASCADE, primary_key=True)
    final_depression = models.CharField(max_length=10, choices=BOOLEAN_CHOICES, null=True, blank=True,
                                        verbose_name='Final Depression',
                                        help_text='Definite (lifetime) presence of at least one DSMIV major '
                                                  'depressive episode')
    depressed_mood = models.CharField(max_length=10, choices=BOOLEAN_CHOICES, null=True, blank=True,
                                      verbose_name='Depressed Mood',
                                      help_text='Persistent depressed mood for 2+ weeks (DSMIV depression '
                                                'symptom – either depressed mood or anhedonia must be present '
                                                'for a major depressive episode)')
    depression_anhedonia = models.CharField(max_length=10, choices=BOOLEAN_CHOICES, null=True, blank=True,
                                            verbose_name='Anhedonia (Depression)',
                                            help_text='Persistent anhedonia for 2+ weeks (DSMIV depression '
                                                      'symptom – either depressed mood or anhedonia must be present '
                                                      'for a major depressive episode)')
    app_wt_change = models.CharField(max_length=10, choices=BOOLEAN_CHOICES, null=True, blank=True,
                                     verbose_name='Appetite / Weight Change',
                                     help_text='Significant appetite and/or weight change during depression '
                                               '(DSMIV depression symptom)')
    sleep_disturb = models.CharField(max_length=10, choices=BOOLEAN_CHOICES, null=True, blank=True,
                                     verbose_name='Sleep Disturbance',
                                     help_text='Significant sleep pattern disturbance – either trouble sleeping '
                                               'or sleeping too much during depression (DSMIV depression symptom)')
    psych_change = models.CharField(max_length=10, choices=BOOLEAN_CHOICES, null=True, blank=True,
                                    verbose_name='Psychomotor Change',
                                    help_text='Psychomotor agitation or retardation during depression '
                                              '(DSMIV depression symptom)')
    fatigue_energyloss = models.CharField(max_length=10, choices=BOOLEAN_CHOICES, null=True, blank=True,
                                          verbose_name='Fatigue / Energy Loss',
                                          help_text='Fatigue or loss of energy during depression '
                                                    '(DSMIV depression symptom)')
    worthless_guilt = models.CharField(max_length=10, choices=BOOLEAN_CHOICES, null=True, blank=True,
                                       verbose_name='Worthlessness / Guilt',
                                       help_text='Persistent feelings of worthlessness or guilt during depression '
                                                 '(DSMIV depression symptom)')
    decreased_conc = models.CharField(max_length=10, choices=BOOLEAN_CHOICES, null=True, blank=True,
                                      verbose_name='Decreased Concentration',
                                      help_text='Decreased concentration during depression '
                                                '(DSMIV depression symptom)')
    death_suicide = models.CharField(max_length=10, choices=BOOLEAN_CHOICES, null=True, blank=True,
                                     verbose_name='Thoughts of Death / Suicide',
                                     help_text='Persistent thoughts of death or suicide during depression '
                                               '(DSMIV depression symptom)')
    depressive_symptoms_count = models.IntegerField(null=True, blank=True, verbose_name='Count of Depressive Symptoms',
                                                    validators=[validate_depression_count],
                                                    help_text='Count of DSMIV depressive symptoms used to establish '
                                                              'the presence/absence of an episode (0-9). '
                                                              'Symptoms are operationalised to correspond with the '
                                                              'DSMIV diagnostic criteria. 5+ required, one of which '
                                                              'must be depressed mood or anhedonia (although presence '
                                                              'of symptoms concurrently does not guarantee a positive '
                                                              'rating for an episode due to time criterion).')


class SymptomsMania(models.Model):
    """
    6. Mania
    """
    clinical = models.OneToOneField(Clinical, on_delete=models.CASCADE, primary_key=True)
    final_mania = models.CharField(max_length=10, choices=BOOLEAN_CHOICES, null=True, blank=True,
                                   verbose_name='Final mania',
                                   help_text='Definite (lifetime) presence of at least one DSMIV manic episode')
    elevated_mood = models.CharField(max_length=10, choices=BOOLEAN_CHOICES, null=True, blank=True,
                                     verbose_name='Elevated / Elated mood',
                                     help_text='Elated mood for 1+ week (or any duration if hospitalised) '
                                               '(either elated or irritable mood must be present for a '
                                               'DSMIV manic episode)')
    irritable_mood = models.CharField(max_length=10, choices=BOOLEAN_CHOICES, null=True, blank=True,
                                      verbose_name='Irritable mood',
                                      help_text='Irritable mood for 1+ week (or any duration if hospitalised) '
                                                '(either elated or irritable mood must be present for a '
                                                'DSMIV manic episode)')
    grandiosity = models.CharField(max_length=10, choices=BOOLEAN_CHOICES, null=True, blank=True,
                                   verbose_name='Grandiosity',
                                   help_text='Grandiosity/inflated self esteem (DSMIV manic symptom)')
    decreased_sleep = models.CharField(max_length=10, choices=BOOLEAN_CHOICES, null=True, blank=True,
                                       verbose_name='Decreased Need for Sleep',
                                       help_text='Decreased need for sleep – feels rested on little or no '
                                                 'sleep (DSMIV manic symptom)')
    pressured_speech = models.CharField(max_length=10, choices=BOOLEAN_CHOICES, null=True, blank=True,
                                        verbose_name='Pressured Speech',
                                        help_text='More talkative or pressured speech (DSMIV manic symptom)')
    racing_thoughts = models.CharField(max_length=10, choices=BOOLEAN_CHOICES, null=True, blank=True,
                                       verbose_name='Racing Thoughts / Flight of Ideas',
                                       help_text='Flight of ideas or subjective racing thoughts '
                                                 '(DSMIV manic symptom)')
    distractibility = models.CharField(max_length=10, choices=BOOLEAN_CHOICES, null=True, blank=True,
                                       verbose_name='Distractibility',
                                       help_text='Distractibility (DSMIV manic symptom)')
    psychmotor_agitation = models.CharField(max_length=10, choices=BOOLEAN_CHOICES, null=True, blank=True,
                                            verbose_name='Psychomotor Agitation',
                                            help_text='Increased goal-oriented activity or '
                                                      'psychomotor agitation (DSMIV manic symptom)')
    risky_behaviour = models.CharField(max_length=10, choices=BOOLEAN_CHOICES, null=True, blank=True,
                                       verbose_name='Risky Behaviour',
                                       help_text='Excessive risky pleasurable behaviour (DSMIV manic symptom)')
    manic_count = models.IntegerField(validators=[validate_manic_count], null=True, blank=True,
                                      verbose_name='Count of Manic Symptoms',
                                      help_text='Count of DSMIV manic symptoms used to establish the presence/absence '
                                                'of an episode (0-7); Symptoms are operationalised to correspond '
                                                'with the DSMIV diagnostic criteria. 3+ required (if elevated mood '
                                                'is present), 4+ required (if only irritable mood is present). '
                                                'One of elevated or irritable mood is essential for a manic episode '
                                                '(note: the presence of symptoms concurrently does not guarantee a '
                                                'positive rating for an episode due to time criterion).')
