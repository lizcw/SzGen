from django.db import models
from datetime import date

FILE_CODES = (
    ('CASEID', 'Case ID'),
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

FIELD_TYPES = (
    (0, 'No'),
    (1, 'Yes (electronic)'),
    (2, 'Yes (hard copy only)'),
    (3, 'Yes (not located)'),
    (9, 'Unknown'),
)

class Dataset(models.Model):
    """
    A Dataset contains information on multiple groups
    """
    id = models.AutoField(primary_key=True)
    group = models.CharField(max_length=60, blank=False, help_text='Data analysis group eg, Australia-MSG1')

    def __str__(self):
        return self.group


class DatasetFile(models.Model):
    """
    Dataset file corresponding to data in DatasetRow with multiple participants
    """
    dataset = models.ForeignKey('Dataset', on_delete=models.CASCADE, related_name='dataset_files')
    type = models.CharField(max_length=100, blank=False, choices=FILE_CODES, help_text='Type of the dataset eg, DIGS file')
    filetype = models.CharField(max_length=60, blank=False, choices=FILE_TYPES, help_text='Digital or Hard copy resource')
    location = models.CharField(max_length=1000, blank=False, help_text='Location of the dataset file either as URL or free text')


class DatasetRow(models.Model):
    """
    A Dataset row has a single participant info but is combined in a Dataset file with a configurable location
    """
    id = models.AutoField(primary_key=True)
    dataset = models.ForeignKey('Dataset', on_delete=models.CASCADE, related_name='dataset_participants')
    participant = models.ForeignKey('StudyParticipant', on_delete=models.CASCADE)
    digs = models.IntegerField(blank=False, default=9, choices=FIELD_TYPES)
    figs = models.IntegerField(blank=False, default=9, choices=FIELD_TYPES)
    narrative = models.IntegerField(blank=False, default=9, choices=FIELD_TYPES)
    records = models.IntegerField(blank=False, default=9, choices=FIELD_TYPES)
    consensus = models.IntegerField(blank=True, null=True, default=9, choices=FIELD_TYPES)
    ldps = models.IntegerField(blank=True, null=True, default=9, choices=FIELD_TYPES)
    notes = models.TextField(verbose_name='Notes', blank=True, null=True)