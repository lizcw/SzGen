# Generated by Django 2.2.3 on 2019-09-09 12:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('szgenapp', '0012_auto_20190909_2019'),
    ]

    operations = [
        migrations.AlterField(
            model_name='harvestsample',
            name='harvest_date',
            field=models.DateField(blank=True, null=True, verbose_name='Harvest Date'),
        ),
        migrations.AlterField(
            model_name='harvestsample',
            name='notes',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='harvestsample',
            name='regrow_date',
            field=models.DateField(blank=True, null=True, verbose_name='Regrow Date'),
        ),
        migrations.AlterField(
            model_name='location',
            name='cell',
            field=models.CharField(blank=True, help_text='Cell number on shelf in tank where sample stored', max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='location',
            name='shelf',
            field=models.CharField(blank=True, help_text='Shelf number in tank where sample stored', max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='location',
            name='tank',
            field=models.CharField(blank=True, help_text='Tank number where sample stored', max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='sample',
            name='notes',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='shipment',
            name='notes',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='shipment',
            name='rutgers_number',
            field=models.CharField(blank=True, help_text='Rutgers Shipment for LCLs', max_length=60, null=True),
        ),
        migrations.AlterField(
            model_name='subsample',
            name='notes',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='transformsample',
            name='notes',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='transformsample',
            name='transform_date',
            field=models.DateField(blank=True, null=True, verbose_name='Transform Date'),
        ),
    ]