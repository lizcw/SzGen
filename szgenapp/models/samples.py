from datetime import date

from django.db import models

SAMPLE_TYPES = (
    (4, 'PLASMA', 'Plasma'),
    (1, 'SERUM', 'Serum'),
    (5, 'PAXGENE', 'PAXgene'),
    (2, 'WB', 'Whole blood'),
    (6, 'SALIVA', 'Saliva'),
    (3, 'UNKNOWN', 'Unknown')
)

SUBSAMPLE_TYPES = (
    ('LCYTE', 'Lymphocyte'),
    ('LCL', 'LCL'),
    ('DNA', 'DNA')
)

class SampleType(models.Model):
    """
    Type of Sample
    """
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30, unique=True, help_text="Value for sample type matched to data")
    description = models.CharField(max_length=50, blank=True, null=True, help_text='Description of sample type')

    def __str__(self):
        return self.name

class Sample(models.Model):
    """
    A blood sample of a participant
    """
    id = models.AutoField(primary_key=True)
    participant = models.ForeignKey('StudyParticipant', on_delete=models.CASCADE, related_name="samples")
    sample_types = models.ManyToManyField(SampleType, help_text='Type of sample')
    rebleed = models.BooleanField(blank=False, default=False)
    arrival_date = models.DateField(verbose_name='Arrival Date', default=date.today, null=True, blank=True,
                                    help_text='Date of sample arrival')
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return 'Sample %d for Participant %s' % (self.id, self.participant.getFullNumber())

    def get_next_subsample_num(self, type):
        """
        Get next sample number for new subsample
        NB Could just return count but may be deleted
        :return:
        """
        next_num = 1
        subsamples = self.subsamples.filter(sample_type=type)
        if subsamples.count() > 0:
            next_num = subsamples.order_by('-sample_num').first().sample_num + 1

        return next_num


class SubSample(models.Model):
    """
    Sub sample derived from sample for further processing
    """
    id = models.AutoField(primary_key=True)
    sample = models.ForeignKey('Sample', on_delete=models.CASCADE, related_name='subsamples')
    sample_num = models.IntegerField(blank=False, default=1, help_text='For example, number 1 of 5 subsamples')
    sample_type = models.CharField(max_length=30, choices=SUBSAMPLE_TYPES, help_text='Type of the sub sample')
    storage_date = models.DateField(verbose_name='Storage Date', blank=True, null=True, help_text="Date stored")
    used = models.BooleanField(default=False, help_text='If used, location should be blank')
    extraction_date = models.DateField(verbose_name='Extraction Date', blank=True, null=True,
                                       help_text='Date of DNA Extraction')
    notes = models.TextField(blank=True, null=True)
    location = models.ForeignKey('Location', blank=True, null=True, on_delete=models.CASCADE)

    def get_qc_result(self):
        if self.sample_qc.count() > 0:
            return self.sample_qc.order_by('-qc_date').first()
        else:
            return None



class Location(models.Model):
    """
    Laboratory location based on Tank / shelf / cell
    """
    id = models.AutoField(primary_key=True)
    tank = models.CharField(max_length=10, blank=True, null=True, help_text='Tank number where sample stored')
    shelf = models.CharField(max_length=10, blank=True, null=True, help_text='Shelf number in tank where sample stored')
    cell = models.CharField(max_length=10, blank=True, null=True, help_text='Cell number on shelf in tank where sample stored')

    def __str__(self):
        if self.tank:
            return '%s/%s/%s' % (self.tank, self.shelf, self.cell)
        else:
            return '0'


class QC(models.Model):
    """
    Quality control for subsamples
    """
    id = models.AutoField(primary_key=True)
    sample = models.ForeignKey('Sample', on_delete=models.CASCADE, related_name='sample_qc')
    qc_date = models.DateField(verbose_name='QC Date', blank=True, null=True,
                               help_text='Date on which quality control ran')
    passed = models.BooleanField(default=False, help_text='True if passed QC')
    notes = models.TextField(blank=True, null=True)


class Shipment(models.Model):
    """
    Shipment details for sending/receiving samples
    """
    id = models.AutoField(primary_key=True)
    sample = models.ForeignKey('Sample', on_delete=models.CASCADE, related_name='shipment')
    shipment_date = models.DateField(verbose_name='Shipment Date', null=False, blank=False,
                                     help_text='Date on which sample shipped')
    reference = models.CharField(max_length=60, null=False, blank=False)
    rutgers_number = models.CharField(max_length=60, blank=True, null=True, help_text='Rutgers Shipment for LCLs')
    notes = models.TextField(null=True, blank=True)


class TransformSample(models.Model):
    """
    Transform process
    """
    id = models.AutoField(primary_key=True)
    sample = models.ForeignKey('Sample', on_delete=models.CASCADE, related_name='transform')
    transform_date = models.DateField(verbose_name='Transform Date', null=True, blank=True)
    failed = models.BooleanField(default=False)
    notes = models.TextField(null=True, blank=True)


class HarvestSample(models.Model):
    """
    Harvest process
    """
    id = models.AutoField(primary_key=True)
    sample = models.ForeignKey('Sample', on_delete=models.CASCADE, related_name='harvest')
    regrow_date = models.DateField(verbose_name='Regrow Date', null=True, blank=True)
    harvest_date = models.DateField(verbose_name='Harvest Date', null=True, blank=True)
    complete = models.BooleanField(default=False)
    notes = models.TextField(null=True, blank=True)
