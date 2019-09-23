import django_tables2 as tables
from django_tables2.utils import A
from szgenapp.models.datasets import *


class DatasetTable(tables.Table):
    id = tables.LinkColumn('dataset_detail', text='View', args=[A('pk')], verbose_name='')
    dataset_count = tables.Column(verbose_name='Files', accessor=A('dataset_files'))
    participant_count = tables.Column(verbose_name='Participants', accessor=A('dataset_participants'))

    class Meta:
        model = Dataset
        template_name = 'django_tables2/bootstrap.html'
        attrs = {"class": "ui-responsive table table-hover"}
        fields = ['id', 'group', 'dataset_count', 'participant_count']

    def render_dataset_count(self, record):
        return record.dataset_files.count()

    def render_participant_count(self, record):
        return record.dataset_participants.count()


class DatasetFileTable(tables.Table):
    id = tables.LinkColumn('dataset_detail', text='View', args=[A('dataset.id')], verbose_name='')
    group = tables.Column(verbose_name='Group', accessor=A('dataset.group'))

    class Meta:
        model = DatasetFile
        template_name = 'django_tables2/bootstrap.html'
        attrs = {"class": "ui-responsive table table-hover"}
        fields = ['id', 'group', 'type', 'filetype', 'location']


class DatasetParticipantTable(tables.Table):
    id = tables.LinkColumn('dataset_participant_update', text='View', args=[A('id')], verbose_name='')
    group = tables.LinkColumn('dataset_detail', args=[A('dataset.id')], accessor=A('dataset.group'))
    participant = tables.LinkColumn('participant_detail', args=[A('participant.id')])


    class Meta:
        model = DatasetRow
        template_name = 'django_tables2/bootstrap.html'
        attrs = {"class": "ui-responsive table table-hover"}
        fields = ['id', 'group', 'participant', 'digs', 'figs', 'narrative', 'records', 'consensus', 'ldps', 'notes']
