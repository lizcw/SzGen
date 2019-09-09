# Generated by Django 2.2.3 on 2019-09-08 01:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('szgenapp', '0007_sub'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='clinical',
            name='demographic',
        ),
        migrations.RemoveField(
            model_name='clinical',
            name='diagnosis',
        ),
        migrations.RemoveField(
            model_name='clinical',
            name='medical',
        ),
        migrations.RemoveField(
            model_name='clinical',
            name='symptoms_behaviour',
        ),
        migrations.RemoveField(
            model_name='clinical',
            name='symptoms_delusion',
        ),
        migrations.RemoveField(
            model_name='clinical',
            name='symptoms_depression',
        ),
        migrations.RemoveField(
            model_name='clinical',
            name='symptoms_general',
        ),
        migrations.RemoveField(
            model_name='clinical',
            name='symptoms_hallucination',
        ),
        migrations.RemoveField(
            model_name='clinical',
            name='symptoms_mania',
        ),
        migrations.RemoveField(
            model_name='demographic',
            name='id',
        ),
        migrations.RemoveField(
            model_name='diagnosis',
            name='id',
        ),
        migrations.RemoveField(
            model_name='medicalhistory',
            name='id',
        ),
        migrations.RemoveField(
            model_name='symptomsbehaviour',
            name='id',
        ),
        migrations.RemoveField(
            model_name='symptomsdelusion',
            name='id',
        ),
        migrations.RemoveField(
            model_name='symptomsdepression',
            name='id',
        ),
        migrations.RemoveField(
            model_name='symptomsgeneral',
            name='id',
        ),
        migrations.RemoveField(
            model_name='symptomshallucination',
            name='id',
        ),
        migrations.RemoveField(
            model_name='symptomsmania',
            name='id',
        ),
        migrations.AddField(
            model_name='demographic',
            name='clinical',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='szgenapp.Clinical'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='diagnosis',
            name='clinical',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='szgenapp.Clinical'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='medicalhistory',
            name='clinical',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='szgenapp.Clinical'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='symptomsbehaviour',
            name='clinical',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='szgenapp.Clinical'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='symptomsdelusion',
            name='clinical',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='szgenapp.Clinical'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='symptomsdepression',
            name='clinical',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='szgenapp.Clinical'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='symptomsgeneral',
            name='clinical',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='szgenapp.Clinical'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='symptomshallucination',
            name='clinical',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='szgenapp.Clinical'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='symptomsmania',
            name='clinical',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='szgenapp.Clinical'),
            preserve_default=False,
        ),
    ]