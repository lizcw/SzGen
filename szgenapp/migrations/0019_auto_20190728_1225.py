# Generated by Django 2.2.3 on 2019-07-28 02:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('szgenapp', '0018_auto_20190727_2133'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='location',
            name='ref',
        ),
        migrations.RemoveField(
            model_name='sample',
            name='stage_type',
        ),
        migrations.RemoveField(
            model_name='sample',
            name='storage_date',
        ),
        migrations.RemoveField(
            model_name='sample',
            name='storage_location',
        ),
        migrations.RemoveField(
            model_name='subsample',
            name='sample_num',
        ),
        migrations.AddField(
            model_name='location',
            name='num',
            field=models.IntegerField(default=1, help_text='For example, number 1 of 5 subsamples'),
        ),
        migrations.AddField(
            model_name='qc',
            name='notes',
            field=models.TextField(blank=True, null=True),
        ),
    ]
