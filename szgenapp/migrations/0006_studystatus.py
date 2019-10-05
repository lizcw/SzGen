# Generated by Django 2.2.5 on 2019-10-05 21:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('szgenapp', '0005_auto_20191006_0710'),
    ]

    operations = [
        migrations.CreateModel(
            name='StudyStatus',
            fields=[
                ('code', models.CharField(help_text='Study Status code', max_length=10, primary_key=True, serialize=False)),
                ('name', models.CharField(help_text='Study Status description', max_length=40)),
            ],
            options={
                'verbose_name': 'Study Status',
                'verbose_name_plural': 'Studies',
            },
        ),
    ]