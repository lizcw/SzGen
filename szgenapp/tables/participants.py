import django_tables2 as tables
from django_tables2.utils import A
from szgenapp.models.participants import *

# class ParticipantTable(tables.Table):
#     """
#     Not used as contains multiple studyparticipants
#     """
#
#     class Meta:
#         model = Participant
#         template_name = 'django_tables2/bootstrap.html'
#         attrs = {"class": "ui-responsive table table-hover"}
#         fields = ['id', 'country', 'status', 'alphacode', 'secondaryid', 'npid']


class StudyParticipantTable(tables.Table):
    """
    List of Participants - filterable by study, id search (all fields), family id
    """
    fullnumber = tables.LinkColumn('participant_detail', args=[A('participant.id')])
    study = tables.LinkColumn('study_detail', verbose_name='Study', args=[A('study.id')])
    country = tables.Column(verbose_name='Country', accessor=A('participant.country'))
    status = tables.Column(verbose_name='Country', accessor=A('participant.status'))
    alphacode = tables.Column(verbose_name='Alpha Code', accessor=A('participant.alphacode'))
    secondaryid = tables.Column(verbose_name='Secondary ID', accessor=A('participant.secondaryid'))
    npid = tables.Column(verbose_name='NeuroPsychiatric ID', accessor=A('participant.npid'))

    class Meta:
        model = StudyParticipant
        template_name = 'django_tables2/bootstrap.html'
        attrs = {"class": "ui-responsive table table-hover"}
        fields = ['fullnumber','study', 'country', 'status', 'family', 'alphacode', 'secondaryid', 'npid']

    def render_study(self, record):
        return record.study.title

