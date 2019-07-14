from django.db import models
from datetime import date
from szgenapp.models import Study

COUNTRY_CHOICES = (
    ('INDIA', 'India'),
    ('AUSTRALIA', 'Australia'),
    ('USA', 'USA'),
    ('UK', 'UK')
)
PARTICIPANT_STATUS_CHOICES = (
    ('CURRENT', 'Current'),
    ('WITHDRAWN', 'Withdrawn'),
    ('DECEASED', 'Deceased'),
    ('UNKNOWN', 'Unknown')
)

class Participant(models.Model):
    id = models.AutoField(primary_key=True)
    study = models.ManyToManyField(Study)
    # Alternative IDs should all be stored here
    district = models.CharField(max_length=5, blank=True, help_text="For CBZ study enter district(1-5)")
    fullnumber = models.CharField(max_length=30, blank=True, help_text="Provide full number if it cannot be generated from parts")
    family = models.CharField(max_length=20, blank=True, help_text="Family number if available")
    individual = models.CharField(max_length=20, blank=True, help_text="Individual number if available")
    alphacode = models.CharField(max_length=30, blank=True, help_text="Alpha code if available")
    secondary = models.CharField(max_length=30, blank=True, help_text="Alternative or additional ID")
    npid = models.CharField(max_length=30, blank=True, help_text="NP ID if available")
    arrival_date = models.DateField(default=date.today, help_text="Date of beginning the study, default is today")
    country = models.CharField(max_length=30, blank=False, choices=COUNTRY_CHOICES)
    status = models.CharField(max_length=20, blank=False, choices=PARTICIPANT_STATUS_CHOICES, default="CURRENT")
    pedigree = models.ManyToManyField("self", blank=True, help_text="Link familial participants here")

    def getFullNumber(self, studycode=""):
        """
        Participant ID as <StudyPrefix>-<FamilyID>-<IndividualID>
        :param studycode: provided as multiple studies possible
        :return: string
        """
        if self.fullnumber:
            return self.fullnumber
        else:
            if studycode == "CBZ" and self.district != None:
                studycode += self.district
            # find study code and add study
            studies = self.study.all()

            if studycode == "":
                parts = [self.family, self.individual]
            else:
                parts = [studycode, self.family, self.individual]
            return "-".join(parts)

    def parseFullNumber(self, fullnumber):
        """
        Parse a full number of format above to appropriate fields (useful on upload only)
        :return:
        """
        parts = fullnumber.split("-")
        if len(parts) == 3:
            self.family = parts[1]
            self.individual = parts[2]
            # find study code and add study
            studies = self.study.all()
            if studies.count() == 0:
                studies = Study.objects.filter(precursor__exact=parts[0])
            if studies.count() == 1:
                self.study.create(studies.first())
                print("study added to participant")
                return studies.first()
            else:
                print("study not found")
                return None

    def __unicode__(self):
        if self.study.all().count() == 1:
            study = self.study.first()
        else:
            study = ''
        return self.getFullNumber(study) + "[" + self.get_status_display() + "]"