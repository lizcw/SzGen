# Generated by Django 2.2.3 on 2019-09-08 01:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('szgenapp', '0006_auto_20190908_1049'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sub',
            fields=[
                ('clinical', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='szgenapp.Clinical')),
                ('comments', models.CharField(max_length=30)),
            ],
        ),
    ]