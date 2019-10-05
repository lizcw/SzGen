from django.contrib import admin
from szgenapp.models.samples import SampleType
from szgenapp.models.participants import Country, Status
from szgenapp.models.studies import StudyStatus
# Register your models here.
admin.site.register(SampleType)
admin.site.register(Country)
admin.site.register(Status)
admin.site.register(StudyStatus)