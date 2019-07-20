# Generated by Django 2.2.3 on 2019-07-20 10:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('szgenapp', '0007_dataset_datasetfile_datasetrow'),
    ]

    operations = [
        migrations.AlterField(
            model_name='datasetfile',
            name='dataset',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dataset_files', to='szgenapp.Dataset'),
        ),
        migrations.AlterField(
            model_name='datasetrow',
            name='dataset',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dataset_groups', to='szgenapp.Dataset'),
        ),
    ]
