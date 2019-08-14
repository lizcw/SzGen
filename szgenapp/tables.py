import django_tables2 as tables
from django_tables2.utils import A
from szgenapp.models.clinical import Clinical


class ClinicalTable(tables.Table):
    id = tables.LinkColumn('clinical_detail', text='View', args=[A('pk')], verbose_name='')
    gender = tables.Column(verbose_name='Gender', accessor=A('demographic.first.gender'))
    diagnosis = tables.Column(verbose_name='Diagnosis', accessor=A('diagnosis.first.summary'))
    school = tables.Column(verbose_name='Years School', accessor=A('demographic.first.years_school'))

    class Meta:
        model = Clinical
        template_name = 'django_tables2/bootstrap.html'
        attrs = {"class": "ui-responsive table table-hover"}
        fields = ['id', 'participant', 'diagnosis']
