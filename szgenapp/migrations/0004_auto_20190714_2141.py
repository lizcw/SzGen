# Generated by Django 2.2.3 on 2019-07-14 11:41

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('szgenapp', '0003_participant'),
    ]

    operations = [
        migrations.AddField(
            model_name='participant',
            name='district',
            field=models.CharField(blank=True, help_text='For CBZ study enter district(1-5)', max_length=5),
        ),
        migrations.AddField(
            model_name='participant',
            name='fullnumber',
            field=models.CharField(blank=True, help_text='Provide full number if it cannot be generated from parts', max_length=30),
        ),
        migrations.AlterField(
            model_name='participant',
            name='alphacode',
            field=models.CharField(blank=True, help_text='Alpha code if available', max_length=30),
        ),
        migrations.AlterField(
            model_name='participant',
            name='arrival_date',
            field=models.DateField(default=datetime.date.today, help_text='Date of beginning the study, default is today'),
        ),
        migrations.AlterField(
            model_name='participant',
            name='family',
            field=models.CharField(blank=True, help_text='Family number if available', max_length=20),
        ),
        migrations.AlterField(
            model_name='participant',
            name='individual',
            field=models.CharField(blank=True, help_text='Individual number if available', max_length=20),
        ),
        migrations.AlterField(
            model_name='participant',
            name='npid',
            field=models.CharField(blank=True, help_text='NP ID if available', max_length=30),
        ),
        migrations.AlterField(
            model_name='participant',
            name='pedigree',
            field=models.ManyToManyField(blank=True, help_text='Link familial participants here', related_name='_participant_pedigree_+', to='szgenapp.Participant'),
        ),
        migrations.AlterField(
            model_name='participant',
            name='secondary',
            field=models.CharField(blank=True, help_text='Alternative or additional ID', max_length=30),
        ),
    ]
