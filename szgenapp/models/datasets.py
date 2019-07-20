from django.db import models
from datetime import date

FIELD_CODES = (
    ('DIGS', 'DIGS'),
    ('FIGS', 'FIGS'),
    ('NARRATIVE', 'Narrative'),
    ('RECORDS', 'Medical Records'),
    ('CONSENSUS', 'Consensus'),
    ('LDPS', 'LDPS')
)

FILE_TYPES = (
    ('DIGITAL', 'Digital'),
    ('HARDCOPY', 'Hard Copy')
)


class Dataset(models.Model):
    """
    A Dataset contains information on multiple groups
    """
    id = models.AutoField(primary_key=True)
    group = models.CharField(max_length=60, blank=False, help_text='Data analysis group eg, Australia-MSG1')


class DatasetFile(models.Model):
    """
    Dataset file corresponding to data in DatasetRow with multiple participants
    """
    dataset = models.ForeignKey('Dataset', on_delete=models.CASCADE, related_name='dataset_files')
    type = models.CharField(max_length=100, blank=False, choices=FIELD_CODES, help_text='Type of the dataset eg, DIGS file')
    filetype = models.CharField(max_length=60, blank=False, help_text='Digital or Hard copy resource', choices=FILE_TYPES)
    location = models.CharField(max_length=1000, blank=False, help_text='Location of the dataset file either as URL or free text')


class DatasetRow(models.Model):
    """
    A Dataset row has a single participant info but is combined in a Dataset file with a configurable location
    """
    id = models.AutoField(primary_key=True)
    dataset = models.ForeignKey('Dataset', on_delete=models.CASCADE, related_name='dataset_participants')
    participant = models.ForeignKey('StudyParticipant', on_delete=models.CASCADE)
    digs = models.IntegerField(blank=False, default=0)
    figs = models.IntegerField(blank=False, default=0)
    narrative = models.IntegerField(blank=False, default=0)
    records = models.IntegerField(blank=False, default=0)
    consensus = models.IntegerField(blank=True, default=0)
    ldps = models.IntegerField(blank=True, default=0)
    notes = models.TextField(verbose_name='Notes', blank=True)