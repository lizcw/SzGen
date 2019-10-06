from django.contrib import admin
from szgenapp.models.samples import SampleType
from szgenapp.models.participants import Country, Status
from szgenapp.models.studies import StudyStatus
from szgenapp.models.clinical import Dsmiv, Employment, EmploymentHistory, Gaf, Gafwl, Gender, Illness, Living, \
    MaritalStatus, Onset,Religious,Severity, SeverityPattern, SymptomPattern
# Register your models here.
admin.site.register(SampleType)
admin.site.register(Country)
admin.site.register(Status)
admin.site.register(StudyStatus)
admin.site.register(Dsmiv)
admin.site.register(Employment)
admin.site.register(EmploymentHistory)
admin.site.register(Gaf)
admin.site.register(Gafwl)
admin.site.register(Gender)
admin.site.register(Illness)
admin.site.register(Living)
admin.site.register(MaritalStatus)
admin.site.register(Onset)
admin.site.register(Religious)
admin.site.register(Severity)
admin.site.register(SeverityPattern)
admin.site.register(SymptomPattern)