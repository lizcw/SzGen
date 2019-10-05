# Generated by Django 2.2.5 on 2019-10-05 21:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('szgenapp', '0007_load_studystatus'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='studystatus',
            options={'verbose_name': 'Study Status', 'verbose_name_plural': 'Study Statuses'},
        ),
        migrations.AlterField(
            model_name='study',
            name='status',
            field=models.ForeignKey(help_text='Status of this study', null=True, on_delete=django.db.models.deletion.SET_NULL, to='szgenapp.StudyStatus'),
        ),
    ]
