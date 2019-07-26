from django.db import models
from datetime import date

COUNTRY_CHOICES = (
    ('INDIA', 'India'),
    ('AUSTRALIA', 'Australia'),
    ('USA', 'USA'),
    ('UK', 'UK')
)
PARTICIPANT_STATUS_CHOICES = (
    ('ACTIVE', 'Active'),
    ('WITHDRAWN', 'Withdrawn'),
    ('DECEASED', 'Deceased'),
    ('UNKNOWN', 'Unknown')
)


class Participant(models.Model):
    """
    A Participant represents a single physical individual who may have multiple IDs from various datasets
    """
    id = models.AutoField(primary_key=True)

    # Static fields
    country = models.CharField(max_length=30, blank=False, choices=COUNTRY_CHOICES)
    status = models.CharField(max_length=20, blank=False, choices=PARTICIPANT_STATUS_CHOICES, default="ACTIVE")
    # Alternative IDs should all be stored here
    alphacode = models.CharField(max_length=30, blank=True, verbose_name="Alpha Code", help_text="Alpha code if available")
    secondaryid = models.CharField(max_length=30, blank=True, verbose_name="Secondary ID",
                                   help_text="Alternative or additional ID if available")
    npid = models.CharField(max_length=30, blank=True, verbose_name="NeuroPsychiatric ID", help_text="NP ID if available")
    # Link other participants - family, duplicates
    pedigree = models.ManyToManyField("self", blank=True, help_text="Link familial participants here")

    class Meta:
        verbose_name = 'Participant'
        verbose_name_plural = 'Participants'

    def __str__(self):
        pid = None
        if (self.studyparticipants.first()):
            pid = self.studyparticipants.first().getFullNumber()
        elif (self.alphacode):
            pid = self.alphacode
        else:
            pid = self.id
        return str(pid) + " (" + self.get_country_display() + ": " + self.get_status_display() + ")"


class StudyParticipant(models.Model):
    """
    A Participant has one or more studies in which they have different IDs
    """
    id = models.AutoField(primary_key=True)
    participant = models.ForeignKey('Participant', on_delete=models.CASCADE, related_name='studyparticipants')
    study = models.ForeignKey('Study', on_delete=models.CASCADE)
    fullnumber = models.CharField(max_length=30, blank=True, verbose_name="Full Number",
                                  help_text="Provide full number if it cannot be generated from parts")
    district = models.CharField(max_length=5, blank=True, help_text="For CBZ study enter district(1-5)")
    family = models.CharField(max_length=20, blank=True, help_text="Family number if available")
    individual = models.CharField(max_length=20, blank=True, help_text="Individual number if available")
    arrival_date = models.DateField(default=date.today, help_text="Date of receiving sample, default is today")

    class Meta:
        verbose_name = 'Study Participant'
        verbose_name_plural = 'Study Participants'

    def __str__(self):
        return '%s' % self.fullnumber

    # def get_absolute_url(self):
    #     return reverse('study_participant', args=[str(self.id)])

    def getFullNumber(self):
        """
        Participant ID as <StudyPrefix>-<FamilyID>-<IndividualID>
        :param studycode: provided as multiple studies possible
        :return: string
        """
        if self.fullnumber:
            return self.fullnumber
        else:
            if self.study.precursor == "CBZ" and self.district is not None:
                parts = [self.study.precursor + self.district, self.family, self.individual]

            if self.study.precursor is None:
                parts = [self.family, self.individual]
            else:
                parts = [self.study.precursor + self.family, self.individual]
            return "-".join(parts)
