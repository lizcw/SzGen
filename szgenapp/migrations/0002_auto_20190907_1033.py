# Generated by Django 2.2.3 on 2019-09-07 00:33

from django.db import migrations, models
import django.db.models.deletion
import szgenapp.validators


class Migration(migrations.Migration):

    dependencies = [
        ('szgenapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('docfile', models.FileField(upload_to='', verbose_name='Document')),
                ('description', models.CharField(blank=True, max_length=200, null=True, verbose_name='Description')),
                ('order', models.SmallIntegerField(default=1, verbose_name='Order')),
                ('archive', models.BooleanField(default=False, verbose_name='Archive')),
            ],
        ),
        migrations.AlterField(
            model_name='datasetfile',
            name='dataset',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dataset_files', to='szgenapp.Dataset', verbose_name='Dataset'),
        ),
        migrations.AlterField(
            model_name='datasetrow',
            name='dataset',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dataset_participants', to='szgenapp.Dataset', verbose_name='dDataset'),
        ),
        migrations.AlterField(
            model_name='diagnosis',
            name='dup',
            field=models.IntegerField(help_text='Period between onset and first treatment (in years)', verbose_name='Duration of Untreated Psychosis (DUP)'),
        ),
        migrations.AlterField(
            model_name='diagnosis',
            name='summary',
            field=models.CharField(blank=True, choices=[('SAD', 'Schizoaffective, depressed'), ('SAM', 'Schizoaffective, bipolar'), ('SZ', 'Schizophrenia')], help_text='DSMIV Diagnosis', max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='symptomsdepression',
            name='depressive_symptoms_count',
            field=models.IntegerField(blank=True, help_text='Count of DSMIV depressive symptoms used to establish the presence/absence of an episode (0-9). Symptoms are operationalised to correspond with the DSMIV diagnostic criteria. 5+ required, one of which must be depressed mood or anhedonia (although presence of symptoms concurrently does not guarantee a positive rating for an episode due to time criterion).', null=True, validators=[szgenapp.validators.validate_depression_count], verbose_name='Count of Depressive Symptoms'),
        ),
    ]
