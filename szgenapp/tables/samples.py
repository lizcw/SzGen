import django_tables2 as tables
from django_tables2.utils import A
from szgenapp.models.samples import Sample, SubSample


class SampleTable(tables.Table):
    id = tables.LinkColumn('sample_detail', text='View', args=[A('pk')], verbose_name='')
    participant = tables.LinkColumn('participant_detail', args=[A('participant.id')],
                                    accessor=A('participant.fullnumber'), verbose_name='Participant')
    shipment = tables.Column(verbose_name="Shipments", accessor=A('shipment'))
    qc = tables.Column(verbose_name="QC", accessor=A('sample_qc'))

    class Meta:
        model = Sample
        template_name = 'django_tables2/bootstrap.html'
        attrs = {"class": "ui-responsive table table-hover"}
        fields = ['id', 'participant', 'arrival_date', 'sample_types', 'rebleed', 'shipment', 'qc','notes']

    def render_shipment(self, record):
        return record.shipment.count()

    def render_qc(self, record):
        return record.sample_qc.count()


class SubSampleTable(tables.Table):
    id = tables.LinkColumn('sample_detail', text='View', verbose_name='', args=[A('sample.id')])
    sample = tables.LinkColumn('participant_detail', verbose_name='Participant',
                               accessor=A('sample.participant.fullnumber'),
                               args=[A('sample.participant.id')])

    class Meta:
        model = SubSample
        template_name = 'django_tables2/bootstrap.html'
        attrs = {"class": "ui-responsive table table-hover"}
        fields = ['id', 'sample', 'sample_type', 'sample_num', 'storage_date', 'used', 'location', 'notes']

    def render_sample(self, record):
        return record.sample.participant

    def render_storage_date(self, value):
        if value is None:
            return '-'
        else:
            return value

class SubSampleDNATable(tables.Table):
    """
    Just fields for DNA
    """
    id = tables.LinkColumn('sample_detail', text='View', verbose_name='', args=[A('sample.id')])
    sample = tables.LinkColumn('participant_detail', verbose_name='Participant',
                               accessor=A('sample.participant.fullnumber'),
                               args=[A('sample.participant.id')])

    class Meta:
        model = SubSample
        template_name = 'django_tables2/bootstrap.html'
        attrs = {"class": "ui-responsive table table-hover"}
        fields = ['id', 'sample', 'sample_type', 'sample_num', 'storage_date', 'extraction_date', 'notes']

    def render_sample(self, record):
        return record.sample.participant

    def render_storage_date(self, value):
        if value is None:
            return '-'
        else:
            return value

    def render_extraction_date(self, value):
        if value is None:
            return '-'
        else:
            return value
