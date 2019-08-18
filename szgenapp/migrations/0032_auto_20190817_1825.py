# Generated by Django 2.2.3 on 2019-08-17 08:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('szgenapp', '0031_auto_20190817_1650'),
    ]

    operations = [
        migrations.AlterField(
            model_name='diagnosis',
            name='dup_approx',
            field=models.BooleanField(default=False, help_text='Period for DUP is approximate (eg 20+)', verbose_name='DUP is approximate'),
        ),
        migrations.AlterField(
            model_name='diagnosis',
            name='hospitalisation',
            field=models.CharField(blank=True, choices=[('Yes', 'Yes'), ('No', 'No'), ('Unk', 'Unknown')], help_text='Whether the individual has ever been hospitalised for psychiatric reasons', max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='diagnosis',
            name='hospitalisation_number_approx',
            field=models.BooleanField(default=False, help_text='Number of hospitalisations is approximate (eg >5)', verbose_name='Number of hospitalisations is approximate'),
        ),
        migrations.AlterField(
            model_name='diagnosis',
            name='illness_duration_approx',
            field=models.BooleanField(default=False, help_text='Period for illness duration is approximate (eg 20+)', verbose_name='Illness duration is approximate'),
        ),
        migrations.AlterField(
            model_name='medicalhistory',
            name='abnormal_bed',
            field=models.CharField(blank=True, choices=[('Yes', 'Yes'), ('No', 'No'), ('Unk', 'Unknown')], help_text="Definite evidence of clinically significant birth complications during individual's birth, or definite delayed developmental milestones", max_length=10, null=True, verbose_name='Abnormal birth or early development'),
        ),
        migrations.AlterField(
            model_name='medicalhistory',
            name='alcohol',
            field=models.CharField(blank=True, choices=[('Yes', 'Yes'), ('No', 'No'), ('Unk', 'Unknown')], help_text='DSMIV lifetime alcohol abuse and/or dependence', max_length=10, null=True, verbose_name='Alcohol Use Disorder'),
        ),
        migrations.AlterField(
            model_name='medicalhistory',
            name='cannabis',
            field=models.CharField(blank=True, choices=[('Yes', 'Yes'), ('No', 'No'), ('Unk', 'Unknown')], help_text='DSMIV lifetime cannabis abuse and/or dependence', max_length=10, null=True, verbose_name='Cannabis Use Disorder'),
        ),
        migrations.AlterField(
            model_name='medicalhistory',
            name='epilepsy',
            field=models.CharField(blank=True, choices=[('Yes', 'Yes'), ('No', 'No'), ('Unk', 'Unknown')], help_text='Definite evidence of epilepsy or clinically significant seizures', max_length=10, null=True, verbose_name='Epilepsy'),
        ),
        migrations.AlterField(
            model_name='medicalhistory',
            name='head_injury',
            field=models.CharField(blank=True, choices=[('Yes', 'Yes'), ('No', 'No'), ('Unk', 'Unknown')], help_text='Definite evidence of a significant head injury (i.e. \xa0serious enough to involve loss of consciousness) (lifetime)', max_length=10, null=True, verbose_name='Head Injury'),
        ),
        migrations.AlterField(
            model_name='medicalhistory',
            name='intellectual_disability',
            field=models.CharField(blank=True, choices=[('Yes', 'Yes'), ('No', 'No'), ('Unk', 'Unknown')], help_text='Intelluctual disability: IQ assessed <75', max_length=10, null=True, verbose_name='Intellectual disability'),
        ),
        migrations.AlterField(
            model_name='medicalhistory',
            name='other_drug',
            field=models.CharField(blank=True, choices=[('Yes', 'Yes'), ('No', 'No'), ('Unk', 'Unknown')], help_text='DSMIV lifetime other illicit drug abuse and/or dependence', max_length=10, null=True, verbose_name='Other Drug Use Disorder'),
        ),
        migrations.AlterField(
            model_name='medicalhistory',
            name='suicide',
            field=models.CharField(blank=True, choices=[('Yes', 'Yes'), ('No', 'No'), ('Unk', 'Unknown')], help_text='Whether the individual has ever attempted suicide', max_length=10, null=True, verbose_name='Suicide Attempts'),
        ),
        migrations.AlterField(
            model_name='medicalhistory',
            name='suicide_serious',
            field=models.CharField(blank=True, choices=[('Yes', 'Yes'), ('No', 'No'), ('Unk', 'Unknown')], help_text="Whether the individual's most serious/severe suicide attempt involved serious intent to die.", max_length=10, null=True, verbose_name='Serious Suicidal Intent'),
        ),
        migrations.AlterField(
            model_name='medicalhistory',
            name='thyroid',
            field=models.CharField(blank=True, choices=[('Yes', 'Yes'), ('No', 'No'), ('Unk', 'Unknown')], help_text='Definite evidence of clinically significant thyroid problems', max_length=10, null=True, verbose_name='Thyroid'),
        ),
        migrations.AlterField(
            model_name='symptomsbehaviour',
            name='disorg_catatonic_behav',
            field=models.CharField(blank=True, choices=[('Yes', 'Yes'), ('No', 'No'), ('Unk', 'Unknown')], help_text='Definite (lifetime) presence of disorganised/catatonic behaviour', max_length=10, null=True, verbose_name='Disorganised/Catatonic Behaviour'),
        ),
        migrations.AlterField(
            model_name='symptomsbehaviour',
            name='disorg_speech',
            field=models.CharField(blank=True, choices=[('Yes', 'Yes'), ('No', 'No'), ('Unk', 'Unknown')], help_text='Definite (lifetime) presence of disorganised speech/positive formal thought disorder', max_length=10, null=True, verbose_name='Disorganised Speech'),
        ),
        migrations.AlterField(
            model_name='symptomsbehaviour',
            name='negative_symptoms',
            field=models.CharField(blank=True, choices=[('Yes', 'Yes'), ('No', 'No'), ('Unk', 'Unknown')], help_text='Definite (lifetime) presence of negative symptoms', max_length=10, null=True, verbose_name='Negative Symptoms'),
        ),
        migrations.AlterField(
            model_name='symptomsdelusion',
            name='biw_delusions',
            field=models.CharField(blank=True, choices=[('Yes', 'Yes'), ('No', 'No'), ('Unk', 'Unknown')], help_text='Presence (lifetime) of thought broadcast/insertion/withdrawal delusions', max_length=10, null=True, verbose_name='Broadcast/Insertion/Withdrawal Delusions'),
        ),
        migrations.AlterField(
            model_name='symptomsdelusion',
            name='bizarre_delusions',
            field=models.CharField(blank=True, choices=[('Yes', 'Yes'), ('No', 'No'), ('Unk', 'Unknown')], help_text='Presence (lifetime) of definitely bizarre delusions', max_length=10, null=True, verbose_name='Bizarre Delusions'),
        ),
        migrations.AlterField(
            model_name='symptomsdelusion',
            name='control_delusions',
            field=models.CharField(blank=True, choices=[('Yes', 'Yes'), ('No', 'No'), ('Unk', 'Unknown')], help_text='Presence (lifetime) of delusions of control of thought or actions', max_length=10, null=True, verbose_name='Control Delusions'),
        ),
        migrations.AlterField(
            model_name='symptomsdelusion',
            name='eroto_delusions',
            field=models.CharField(blank=True, choices=[('Yes', 'Yes'), ('No', 'No'), ('Unk', 'Unknown')], help_text='Presence (lifetime) of erotomanic delusions', max_length=10, null=True, verbose_name='Erotomanic Delusions'),
        ),
        migrations.AlterField(
            model_name='symptomsdelusion',
            name='final_delusions',
            field=models.CharField(blank=True, choices=[('Yes', 'Yes'), ('No', 'No'), ('Unk', 'Unknown')], help_text='Definite (lifetime) presence of delusions', max_length=10, null=True, verbose_name='Final Delusions'),
        ),
        migrations.AlterField(
            model_name='symptomsdelusion',
            name='grandiose_delusions',
            field=models.CharField(blank=True, choices=[('Yes', 'Yes'), ('No', 'No'), ('Unk', 'Unknown')], help_text='Presence (lifetime) of grandiose delusions', max_length=10, null=True, verbose_name='Grandiose delusions'),
        ),
        migrations.AlterField(
            model_name='symptomsdelusion',
            name='guilt_sin_delusions',
            field=models.CharField(blank=True, choices=[('Yes', 'Yes'), ('No', 'No'), ('Unk', 'Unknown')], help_text='Presence (lifetime) of guilt or sin delusions', max_length=10, null=True, verbose_name='Guilt/Sin Delusions'),
        ),
        migrations.AlterField(
            model_name='symptomsdelusion',
            name='jealousy_delusions',
            field=models.CharField(blank=True, choices=[('Yes', 'Yes'), ('No', 'No'), ('Unk', 'Unknown')], help_text='Presence (lifetime) of delusions of jealousy', max_length=10, null=True, verbose_name='Jealousy Delusions'),
        ),
        migrations.AlterField(
            model_name='symptomsdelusion',
            name='mindread_delusions',
            field=models.CharField(blank=True, choices=[('Yes', 'Yes'), ('No', 'No'), ('Unk', 'Unknown')], help_text="Presence (lifetime) of delusions of mind reading (of individual's mind by others)", max_length=10, null=True, verbose_name='Mind Reading Delusions'),
        ),
        migrations.AlterField(
            model_name='symptomsdelusion',
            name='persecutory_delusions',
            field=models.CharField(blank=True, choices=[('Yes', 'Yes'), ('No', 'No'), ('Unk', 'Unknown')], help_text='Presence (lifetime) of persecutory delusions', max_length=10, null=True, verbose_name='Persecutory Delusions'),
        ),
        migrations.AlterField(
            model_name='symptomsdelusion',
            name='reference_delusions',
            field=models.CharField(blank=True, choices=[('Yes', 'Yes'), ('No', 'No'), ('Unk', 'Unknown')], help_text='Presence (lifetime) of delusions of reference', max_length=10, null=True, verbose_name='Referential delusions'),
        ),
        migrations.AlterField(
            model_name='symptomsdelusion',
            name='somatic_delusions',
            field=models.CharField(blank=True, choices=[('Yes', 'Yes'), ('No', 'No'), ('Unk', 'Unknown')], help_text='Presence (lifetime) of somatic delusions', max_length=10, null=True, verbose_name='Somatic Delusions'),
        ),
        migrations.AlterField(
            model_name='symptomsdepression',
            name='app_wt_change',
            field=models.CharField(blank=True, choices=[('Yes', 'Yes'), ('No', 'No'), ('Unk', 'Unknown')], help_text='Significant appetite and/or weight change during depression (DSMIV depression symptom)', max_length=10, null=True, verbose_name='Appetite/Weight Change'),
        ),
        migrations.AlterField(
            model_name='symptomsdepression',
            name='death_suicide',
            field=models.CharField(blank=True, choices=[('Yes', 'Yes'), ('No', 'No'), ('Unk', 'Unknown')], help_text='Persistent thoughts of death or suicide during depression (DSMIV depression symptom)', max_length=10, null=True, verbose_name='Thoughts of Death/Suicide'),
        ),
        migrations.AlterField(
            model_name='symptomsdepression',
            name='decreased_conc',
            field=models.CharField(blank=True, choices=[('Yes', 'Yes'), ('No', 'No'), ('Unk', 'Unknown')], help_text='Decreased concentration during depression (DSMIV depression symptom)', max_length=10, null=True, verbose_name='Decreased Concentration'),
        ),
        migrations.AlterField(
            model_name='symptomsdepression',
            name='decreased_sleep',
            field=models.CharField(blank=True, choices=[('Yes', 'Yes'), ('No', 'No'), ('Unk', 'Unknown')], help_text='Decreased need for sleep – feels rested on little or no sleep (DSMIV manic symptom)', max_length=10, null=True, verbose_name='Decreased Need for Sleep'),
        ),
        migrations.AlterField(
            model_name='symptomsdepression',
            name='depressed_mood',
            field=models.CharField(blank=True, choices=[('Yes', 'Yes'), ('No', 'No'), ('Unk', 'Unknown')], help_text='Persistent depressed mood for 2+ weeks (DSMIV depression symptom – either depressed mood or anhedonia must be present for a major depressive episode)', max_length=10, null=True, verbose_name='Depressed Mood'),
        ),
        migrations.AlterField(
            model_name='symptomsdepression',
            name='depression_anhedonia',
            field=models.CharField(blank=True, choices=[('Yes', 'Yes'), ('No', 'No'), ('Unk', 'Unknown')], help_text='Persistent anhedonia for 2+ weeks (DSMIV depression symptom – either depressed mood or anhedonia must be present for a major depressive episode)', max_length=10, null=True, verbose_name='Anhedonia (Depression)'),
        ),
        migrations.AlterField(
            model_name='symptomsdepression',
            name='distractibility',
            field=models.CharField(blank=True, choices=[('Yes', 'Yes'), ('No', 'No'), ('Unk', 'Unknown')], help_text='Distractibility (DSMIV manic symptom)', max_length=10, null=True, verbose_name='Distractibility'),
        ),
        migrations.AlterField(
            model_name='symptomsdepression',
            name='elevated_mood',
            field=models.CharField(blank=True, choices=[('Yes', 'Yes'), ('No', 'No'), ('Unk', 'Unknown')], help_text='Elated mood for 1+ week (or any duration if hospitalised) (either elated or irritable mood must be present for a DSMIV manic episode)', max_length=10, null=True, verbose_name='Elevated/Elated mood'),
        ),
        migrations.AlterField(
            model_name='symptomsdepression',
            name='fatigue_energyloss',
            field=models.CharField(blank=True, choices=[('Yes', 'Yes'), ('No', 'No'), ('Unk', 'Unknown')], help_text='Fatigue or loss of energy during depression (DSMIV depression symptom)', max_length=10, null=True, verbose_name='Fatigue/Energy Loss'),
        ),
        migrations.AlterField(
            model_name='symptomsdepression',
            name='final_depression',
            field=models.CharField(blank=True, choices=[('Yes', 'Yes'), ('No', 'No'), ('Unk', 'Unknown')], help_text='Definite (lifetime) presence of at least one DSMIV major depressive episode', max_length=10, null=True, verbose_name='Final Depression'),
        ),
        migrations.AlterField(
            model_name='symptomsdepression',
            name='final_mania',
            field=models.CharField(blank=True, choices=[('Yes', 'Yes'), ('No', 'No'), ('Unk', 'Unknown')], help_text='Definite (lifetime) presence of at least one DSMIV manic episode', max_length=10, null=True, verbose_name='Final mania'),
        ),
        migrations.AlterField(
            model_name='symptomsdepression',
            name='grandiosity',
            field=models.CharField(blank=True, choices=[('Yes', 'Yes'), ('No', 'No'), ('Unk', 'Unknown')], help_text='Grandiosity/inflated self esteem (DSMIV manic symptom)', max_length=10, null=True, verbose_name='Grandiosity'),
        ),
        migrations.AlterField(
            model_name='symptomsdepression',
            name='irritable_mood',
            field=models.CharField(blank=True, choices=[('Yes', 'Yes'), ('No', 'No'), ('Unk', 'Unknown')], help_text='Irritable mood for 1+ week (or any duration if hospitalised) (either elated or irritable mood must be present for a DSMIV manic episode)', max_length=10, null=True, verbose_name='Irritable mood'),
        ),
        migrations.AlterField(
            model_name='symptomsdepression',
            name='pressured_speech',
            field=models.CharField(blank=True, choices=[('Yes', 'Yes'), ('No', 'No'), ('Unk', 'Unknown')], help_text='More talkative or pressured speech (DSMIV manic symptom)', max_length=10, null=True, verbose_name='Pressured Speech'),
        ),
        migrations.AlterField(
            model_name='symptomsdepression',
            name='psych_change',
            field=models.CharField(blank=True, choices=[('Yes', 'Yes'), ('No', 'No'), ('Unk', 'Unknown')], help_text='Psychomotor agitation or retardation during depression (DSMIV depression symptom)', max_length=10, null=True, verbose_name='Psychomotor Change'),
        ),
        migrations.AlterField(
            model_name='symptomsdepression',
            name='psychmotor_agitation',
            field=models.CharField(blank=True, choices=[('Yes', 'Yes'), ('No', 'No'), ('Unk', 'Unknown')], help_text='Increased goal-oriented activity or psychomotor agitation (DSMIV manic symptom)', max_length=10, null=True, verbose_name='Psychomotor Agitation'),
        ),
        migrations.AlterField(
            model_name='symptomsdepression',
            name='racing_thoughts',
            field=models.CharField(blank=True, choices=[('Yes', 'Yes'), ('No', 'No'), ('Unk', 'Unknown')], help_text='Flight of ideas or subjective racing thoughts (DSMIV manic symptom)', max_length=10, null=True, verbose_name='Racing Thoughts/Flight of Ideas'),
        ),
        migrations.AlterField(
            model_name='symptomsdepression',
            name='risky_behaviour',
            field=models.CharField(blank=True, choices=[('Yes', 'Yes'), ('No', 'No'), ('Unk', 'Unknown')], help_text='Excessive risky pleasurable behaviour (DSMIV manic symptom)', max_length=10, null=True, verbose_name='Risky Behaviour'),
        ),
        migrations.AlterField(
            model_name='symptomsdepression',
            name='sleep_disturb',
            field=models.CharField(blank=True, choices=[('Yes', 'Yes'), ('No', 'No'), ('Unk', 'Unknown')], help_text='Significant sleep pattern disturbance – either trouble sleeping or sleeping too much during depression (DSMIV depression symptom)', max_length=10, null=True, verbose_name='Sleep Disturbance'),
        ),
        migrations.AlterField(
            model_name='symptomsdepression',
            name='worthless_guilt',
            field=models.CharField(blank=True, choices=[('Yes', 'Yes'), ('No', 'No'), ('Unk', 'Unknown')], help_text='Persistent feelings of worthlessness or guilt during depression (DSMIV depression symptom)', max_length=10, null=True, verbose_name='Worthlessness/Guilt'),
        ),
        migrations.AlterField(
            model_name='symptomsgeneral',
            name='clozapine_status',
            field=models.CharField(blank=True, choices=[('Yes', 'Yes'), ('No', 'No'), ('Unk', 'Unknown')], help_text='Whether the individual is definitely taking clozapine at the time of assessment (Mandatory)', max_length=10, null=True, verbose_name='Clozapine Status'),
        ),
        migrations.AlterField(
            model_name='symptomsgeneral',
            name='current_ap_medication',
            field=models.CharField(blank=True, choices=[('Yes', 'Yes'), ('No', 'No'), ('Unk', 'Unknown')], help_text='Whether the individual is definitely taking antipsychotic medication at the time of assessment', max_length=10, null=True, verbose_name='Current Antipsychotic medication'),
        ),
        migrations.AlterField(
            model_name='symptomsgeneral',
            name='treatment_resistant',
            field=models.CharField(blank=True, choices=[('Yes', 'Yes'), ('No', 'No'), ('Unk', 'Unknown')], help_text='Whether the individual meets strictly defined criteria for treatment resistance (Mandatory)', max_length=10, null=True, verbose_name='Treatment Resistant'),
        ),
        migrations.AlterField(
            model_name='symptomshallucination',
            name='auditory_commentary_hallucinations',
            field=models.CharField(blank=True, choices=[('Yes', 'Yes'), ('No', 'No'), ('Unk', 'Unknown')], help_text='Presence (lifetime) of auditory hallucinations involving commentary or third person conversations between voices', max_length=10, null=True, verbose_name='Commentary/3rd Person Auditory Hallucinations'),
        ),
        migrations.AlterField(
            model_name='symptomshallucination',
            name='auditory_hallucinations',
            field=models.CharField(blank=True, choices=[('Yes', 'Yes'), ('No', 'No'), ('Unk', 'Unknown')], help_text='Presence (lifetime) of auditory hallucinations', max_length=10, null=True, verbose_name='Auditory hallucinations'),
        ),
        migrations.AlterField(
            model_name='symptomshallucination',
            name='final_hallucinations',
            field=models.CharField(blank=True, choices=[('Yes', 'Yes'), ('No', 'No'), ('Unk', 'Unknown')], help_text='Definite (lifetime) presence of hallucinations', max_length=10, null=True, verbose_name='Final Hallucinations'),
        ),
        migrations.AlterField(
            model_name='symptomshallucination',
            name='olf_gust_hallucinations',
            field=models.CharField(blank=True, choices=[('Yes', 'Yes'), ('No', 'No'), ('Unk', 'Unknown')], help_text='Presence (lifetime) of olfactory or gustatory hallucinations', max_length=10, null=True, verbose_name='Olfactory/Gustatory Hallucinations'),
        ),
        migrations.AlterField(
            model_name='symptomshallucination',
            name='somatic_hallucinations',
            field=models.CharField(blank=True, choices=[('Yes', 'Yes'), ('No', 'No'), ('Unk', 'Unknown')], help_text='Presence (lifetime) of somatic/tactile hallucinations', max_length=10, null=True, verbose_name='Somatic/Tactile Hallucinations'),
        ),
        migrations.AlterField(
            model_name='symptomshallucination',
            name='visual_hallucinations',
            field=models.CharField(blank=True, choices=[('Yes', 'Yes'), ('No', 'No'), ('Unk', 'Unknown')], help_text='Presence (lifetime) of visual hallucinations', max_length=10, null=True, verbose_name='Visual Hallucinations'),
        ),
    ]