import django_tables2 as tables
from django_tables2.utils import A
from szgenapp.models.participants import *


class StudyParticipantTable(tables.Table):
    """
    List of Participants - filterable by study, id search (all fields), family id
    """
    fullnumber = tables.LinkColumn('participant_detail',
                                   verbose_name="Participant", args=[A('pk')])
    study = tables.LinkColumn('study_detail', accessor=A('study.title'), verbose_name='Study', args=[A('study.id')])
    country = tables.Column(verbose_name='Country', accessor=A('country'))
    status = tables.Column(verbose_name='Status', accessor=A('status'))
    alphacode = tables.Column(verbose_name='Alpha Code', accessor=A('alphacode'))
    accessid = tables.Column(verbose_name='AccessDB', accessor=A('accessid'))
    samples = tables.Column(verbose_name="Samples", accessor=A('samples'))
    clinical = tables.Column(verbose_name="Clinical", accessor=A('clinical'))

    class Meta:
        model = StudyParticipant
        template_name = 'django_tables2/bootstrap.html'
        attrs = {"class": "ui-responsive table table-hover"}
        fields = ['fullnumber','study', 'country', 'status', 'family', 'individual',
                  'alphacode', 'accessid']

    def render_study(self, record):
        return record.study.title

    def render_samples(self, record):
        return record.samples.count()

    def render_clinical(self, record):
        return record.clinical.count()

