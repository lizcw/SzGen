from django.db import models
from datetime import date

COUNTRY_CHOICES = (
    ('AUS', 'Australia'),
    ('FIJ', 'Fiji'),
    ('IND', 'India'),
    ('MAL', 'Malaysia'),
    ('UNK', 'Unknown')
)
PARTICIPANT_STATUS_CHOICES = (
    ('ACTIVE', 'Active'),
    ('WITHDRAWN', 'Withdrawn'),
    ('DECEASED', 'Deceased'),
    ('UNKNOWN', 'Unknown')
)


class StudyParticipant(models.Model):
    """
    A Participant represents a single physical individual who may have multiple IDs from various datasets
    """
    id = models.AutoField(primary_key=True)
    # Static fields
    country = models.CharField(max_length=30, blank=False, choices=COUNTRY_CHOICES, help_text='Participant Country')
    status = models.CharField(max_length=20, blank=False, choices=PARTICIPANT_STATUS_CHOICES, default="ACTIVE",
                              help_text='Participant status')
    # Alternative IDs should all be stored here
    alphacode = models.CharField(max_length=30, blank=True, verbose_name="Alpha Code", null=True,
                                 help_text="Alpha code if available")
    accessid = models.CharField(max_length=30, blank=True, verbose_name="AccessDB ID", null=True,
                                help_text="ID from Samples Access DB")
    secondaryid = models.CharField(max_length=30, blank=True, verbose_name="Secondary ID", null=True,
                                   help_text="Alternative or additional ID if available")
    npid = models.CharField(max_length=30, blank=True, verbose_name="NeuroPsychiatric ID", null=True,
                            help_text="NP ID if available")
    study = models.ForeignKey('Study', on_delete=models.CASCADE)
    fullnumber = models.CharField(max_length=30, verbose_name="Full Number", unique=True,
                                  help_text="Provide full number if it cannot be generated from parts")
    district = models.CharField(max_length=5, blank=True, null=True,  verbose_name="CBZ Study District",
                                help_text="For CBZ study enter district(1-5)")
    family = models.CharField(max_length=20, blank=True, null=True, help_text="Family number if available")
    individual = models.CharField(max_length=20, blank=True, null=True, help_text="Individual number if available")
    notes = models.CharField(max_length=250, blank=True, null=True, help_text="Notes on individual")
    related_participant = models.ManyToManyField('self', related_name='related_participants')

    class Meta:
        verbose_name = 'Participant'
        verbose_name_plural = 'Participants'

    def __str__(self):
        return '%s' % self.getFullNumber()

    # def get_absolute_url(self):
    #     return reverse('study_participant', args=[str(self.id)])

    def getFullNumber(self):
        """
        Participant ID as <StudyPrefix>-<FamilyID>-<IndividualID>
        :param studycode: provided as multiple studies possible
        :return: string
        """
        if len(self.fullnumber) > 0:
            parts = [self.fullnumber]
        else:
            if self.study.precursor == "CBZ" and self.district is not None:
                parts = [self.study.precursor + self.district, self.family, self.individual]

            elif self.study.precursor is None or self.study.precursor == '':
                parts = [self.family, self.individual]
            else:
                parts = [self.study.precursor + self.family, self.individual]
        return "-".join(parts)
