# Generated by Django 2.2.3 on 2019-07-27 11:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('szgenapp', '0017_auto_20190727_2050'),
    ]

    operations = [
        migrations.AlterField(
            model_name='qc',
            name='qc_date',
            field=models.DateField(blank=True, help_text='Date on which quality control ran', null=True, verbose_name='QC Date'),
        ),
    ]