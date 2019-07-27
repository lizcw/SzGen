from django.db import models
from datetime import date

SAMPLE_TYPES = (
    ('PLASMA', 'Plasma'),
    ('SERUM', 'Serum'),
    ('PAXGENE', 'PAXGene'),
    ('WB', 'Whole blood')
)

SUBSAMPLE_TYPES = (
    ('LCYTE', 'Lymphocyte'),
    ('LCL', 'LCL'),
    ('DNA', 'DNA')
)

STAGE_TYPES = (
    ('HARVEST', 'Harvest'),
    ('GROW', 'Grow'),
    ('REGROW', 'Regrow'),
    ('TRANSFORM', 'Transform'),
    ('COMPLETE', 'Complete'),
    ('UNKNOWN', 'Unknown')
)


class Sample(models.Model):
    """
    A blood sample of a participant
    """
    id = models.AutoField(primary_key=True)
    participant = models.ForeignKey('StudyParticipant', on_delete=models.CASCADE)
    sample_type = models.CharField(max_length=60, blank=False,
                                   choices=SAMPLE_TYPES, help_text='Type of blood sample')
    stage_type = models.CharField(max_length=30, choices=STAGE_TYPES, help_text='Processing Stage of sample')
    rebleed = models.BooleanField(blank=False, default=False)
    storage_date = models.DateField(verbose_name='Storage Date', auto_now_add=True, blank=True)
    storage_location = models.ForeignKey('Location', verbose_name='Location', blank=True, on_delete=models.CASCADE)
    notes = models.TextField(blank=True)

    def __str__(self):
        return 'Sample %d for Participant %s' % (self.id, self.participant.getFullNumber())


class Location(models.Model):
    """
    Laboratory location based on Tank / shelf / cell
    """
    id = models.AutoField(primary_key=True)
    tank = models.CharField(max_length=10, blank=True, help_text='Tank number where sample stored')
    shelf = models.CharField(max_length=10, blank=True, help_text='Shelf number in tank where sample stored')
    cell = models.CharField(max_length=10, blank=True, help_text='Cell number on shelf in tank where sample stored')
    ref = models.CharField(max_length=30, blank=True, help_text='Alternative reference')

    def __str__(self):
        if self.tank:
            return '%s/%s/%s' % (self.tank, self.shelf, self.cell)
        else:
            return self.ref


class QC(models.Model):
    """
    Quality control for subsamples
    """
    id = models.AutoField(primary_key=True)
    subsample = models.ForeignKey('SubSample', on_delete=models.CASCADE, related_name='sample_qc')
    qc_date = models.DateField(verbose_name='QC Date', blank=True, null=True,
                               help_text='Date on which quality control ran')
    passed = models.BooleanField(default=True, help_text='True if passed QC')


class SubSample(models.Model):
    """
    Sub sample derived from sample for further processing
    """
    id = models.AutoField(primary_key=True)
    sample = models.ForeignKey('Sample', on_delete=models.CASCADE)
    sample_num = models.IntegerField(blank=False, default=1, help_text='For example, number 1 of 5 subsamples')
    sample_type = models.CharField(max_length=30, choices=SUBSAMPLE_TYPES, help_text='Type of the sub sample')
    used = models.BooleanField(default=False, help_text='If used, location should be blank')
    storage_date = models.DateField(verbose_name='Storage Date', blank=True, null=True, help_text="Date stored")
    used_date = models.DateField(verbose_name='Used Date', blank=True, null=True, help_text="Date sample used")
    extraction_date = models.DateField(verbose_name='Extraction Date', blank=True, null=True,
                                       help_text='Date of DNA Extraction')
    notes = models.TextField(blank=True)
    location = models.ForeignKey('Location', blank=True, null=True, on_delete=models.CASCADE)

    def get_QC_final(self):
        if self.sample_qc.count() > 0:
            return self.sample_qc.order_by('-qc_date').first()
        else:
            return None


class Shipment(models.Model):
    """
    Shipment details for sending/receiving samples
    """
    id = models.AutoField(primary_key=True)
    sample = models.ForeignKey('Sample', on_delete=models.CASCADE)
    shipment_date = models.DateField(verbose_name='Shipment Date', auto_now_add=True, blank=False,
                                     help_text='Date on which sample shipped')
    reference = models.CharField(max_length=60, blank=False)
    notes = models.TextField(blank=True)
    rutgers_number = models.CharField(max_length=60, blank=True, help_text='Rutgers Shipment No')
    rutgers = models.BooleanField(default=False, help_text='Whether shipped to Rutgers')


class TransformSample(models.Model):
    """
    Transform process
    """
    id = models.AutoField(primary_key=True)
    sample = models.ForeignKey('Sample', on_delete=models.CASCADE)
    transform_date = models.DateField(verbose_name='Transform Date', blank=True)
    failed = models.BooleanField(default=False)
    notes = models.TextField(blank=True)


class HarvestSample(models.Model):
    """
    Harvest process
    """
    id = models.AutoField(primary_key=True)
    sample = models.ForeignKey('Sample', on_delete=models.CASCADE)
    regrow_date = models.DateField(verbose_name='Regrow Date', blank=True)
    harvest_date = models.DateField(verbose_name='Harvest Date', blank=True)
    complete = models.BooleanField(default=False)
    notes = models.TextField(blank=True)
