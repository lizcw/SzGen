# Generated by Django 2.2.3 on 2019-07-14 11:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('szgenapp', '0002_study_notes'),
    ]

    operations = [
        migrations.CreateModel(
            name='Participant',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('alphacode', models.CharField(blank=True, max_length=30)),
                ('family', models.CharField(blank=True, max_length=20)),
                ('individual', models.CharField(blank=True, max_length=20)),
                ('secondary', models.CharField(blank=True, max_length=30)),
                ('npid', models.CharField(blank=True, max_length=30)),
                ('arrival_date', models.DateField(auto_now=True)),
                ('country', models.CharField(choices=[('INDIA', 'India'), ('AUSTRALIA', 'Australia'), ('USA', 'USA'), ('UK', 'UK')], max_length=30)),
                ('status', models.CharField(choices=[('CURRENT', 'Current'), ('WITHDRAWN', 'Withdrawn'), ('DECEASED', 'Deceased'), ('UNKNOWN', 'Unknown')], default='CURRENT', max_length=20)),
                ('pedigree', models.ManyToManyField(blank=True, related_name='_participant_pedigree_+', to='szgenapp.Participant')),
                ('study', models.ManyToManyField(to='szgenapp.Study')),
            ],
        ),
    ]