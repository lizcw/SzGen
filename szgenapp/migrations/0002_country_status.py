# Generated by Django 2.2.5 on 2019-10-05 20:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('szgenapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('code', models.CharField(help_text='Country code', max_length=10, primary_key=True, serialize=False)),
                ('name', models.CharField(help_text='Country name', max_length=40)),
            ],
            options={
                'verbose_name': 'Country',
                'verbose_name_plural': 'Countries',
            },
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('code', models.CharField(help_text='Status code', max_length=10, primary_key=True, serialize=False)),
                ('name', models.CharField(help_text='Status name', max_length=40)),
            ],
            options={
                'verbose_name': 'Status',
                'verbose_name_plural': 'Statuses',
            },
        ),
    ]