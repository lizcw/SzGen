# Generated by Django 2.2.5 on 2019-10-05 21:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('szgenapp', '0008_auto_20191006_0742'),
    ]

    operations = [
        migrations.AddField(
            model_name='sampletype',
            name='description',
            field=models.CharField(blank=True, help_text='Description of sample type', max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='sampletype',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='sampletype',
            name='name',
            field=models.CharField(help_text='Value for sample type matched to data', max_length=30, unique=True),
        ),
    ]
