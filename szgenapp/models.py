from django.db import models
from django.urls import reverse

STATUS_CHOICES = (('STUDY_COMPLETED', 'Completed'),
                      ('STUDY_ONGOING', 'Ongoing'),
                      ('STUDY_NOTFUNDED', 'Not funded'),
                      ('STUDY_OMIT', 'Omit'))

class Study(models.Model):

    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=60, blank=False)
    precursor = models.CharField(max_length=10, blank=False)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ('precursor',)
        verbose_name = 'Study'
        verbose_name_plural = 'Studies'

    def __str__(self):
        return '[%s] %s' % (self.status, self.title)

    def get_absolute_url(self):
        return reverse('study_detail', args=[str(self.id)])