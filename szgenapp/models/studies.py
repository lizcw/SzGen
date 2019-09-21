from django.db import models
from django.urls import reverse

STATUS_CHOICES = (('Completed', 'Completed'),
                  ('Ongoing', 'Ongoing'),
                  ('Not funded', 'Not funded'),
                  ('Omit', 'Omit'))


class Study(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=60, blank=False)
    precursor = models.CharField(max_length=10, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ('precursor',)
        verbose_name = 'Study'
        verbose_name_plural = 'Studies'

    def __str__(self):
        return '[%s] %s' % (self.get_status_display(), self.title)

    def get_absolute_url(self):
        return reverse('study_detail', args=[str(self.id)])
