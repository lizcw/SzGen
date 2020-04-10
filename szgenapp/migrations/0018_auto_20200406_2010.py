# Generated by Django 2.2.5 on 2020-04-06 10:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('szgenapp', '0017_document_help'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sample',
            name='sample_location',
        ),
        migrations.AddField(
            model_name='sample',
            name='plasma_location',
            field=models.CharField(blank=True, help_text='Location of plasma sample', max_length=60, null=True, verbose_name='Plasma Location'),
        ),
        migrations.AddField(
            model_name='sample',
            name='serum_location',
            field=models.CharField(blank=True, help_text='Location of serum sample', max_length=60, null=True, verbose_name='Serum Location'),
        ),
        migrations.AlterField(
            model_name='document',
            name='help',
            field=models.BooleanField(default=False, help_text='Display document on Custom Help Pages', verbose_name='Link to Help'),
        ),
    ]