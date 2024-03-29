from django.db import models
from django.urls import reverse

from szgenapp.models.samples import Sample
from szgenapp.models.clinical import Clinical

STATUS_CHOICES = (('Completed', 'Completed'),
                  ('Ongoing', 'Ongoing'),
                  ('Not funded', 'Not funded'),
                  ('Omit', 'Omit'))

class StudyStatus(models.Model):
    code = models.CharField(primary_key=True, max_length=10, blank=False, null=False, help_text='Study Status code')
    name = models.CharField(max_length=40, blank=False, null=False, help_text='Study Status description')

    class Meta:
        verbose_name = 'Study Status'
        verbose_name_plural = 'Study Statuses'

    def __str__(self):
        return '%s' % self.name

class Study(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=60, blank=False)
    precursor = models.CharField(max_length=10, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    status = models.ForeignKey(StudyStatus, on_delete=models.SET_NULL, null=True, help_text='Status of this study')
    notes = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ('precursor',)
        verbose_name = 'Study'
        verbose_name_plural = 'Studies'

    def __str__(self):
        return '[%s] %s' % (self.status, self.title)

    def get_absolute_url(self):
        return reverse('study_detail', args=[str(self.id)])

    def get_sample_count(self):
        samples = Sample.objects.filter(participant__study__id__exact=self.id)
        return samples.count()

    def get_clinical_count(self):
        clinical = Clinical.objects.filter(participant__study__id__exact=self.id)
        return clinical.count()
