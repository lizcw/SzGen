import django_tables2 as tables
from django_tables2.utils import A
from szgenapp.models.samples import Sample, SubSample


class SampleTable(tables.Table):
    id = tables.LinkColumn('sample_detail', text='View', args=[A('pk')], verbose_name='')
    participant = tables.LinkColumn('participant_detail', args=[A('participant.participant.id')])

    class Meta:
        model = Sample
        template_name = 'django_tables2/bootstrap.html'
        attrs = {"class": "ui-responsive table table-hover"}
        fields = ['id', 'participant', 'arrival_date', 'sample_type', 'rebleed', 'notes']


class SubSampleTable(tables.Table):
    id = tables.LinkColumn('sample_detail', text='View', verbose_name='', args=[A('sample.id')])
    sample = tables.LinkColumn('participant_detail', verbose_name='Participant',
                               args=[A('sample.participant.participant.id')])

    class Meta:
        model = SubSample
        template_name = 'django_tables2/bootstrap.html'
        attrs = {"class": "ui-responsive table table-hover"}
        fields = ['id', 'sample', 'sample_type', 'sample_num', 'storage_date', 'used', 'used_date', 'location', 'notes']

    def render_sample(self, record):
        return record.sample.participant

    def render_storage_date(self, value):
        if value is None:
            return ''
        else:
            return value
