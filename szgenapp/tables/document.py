import django_tables2 as tables
from django_tables2.utils import A
from szgenapp.models.document import Document


class DocumentTable(tables.Table):
    id = tables.LinkColumn('documents_detail', text='View', args=[A('pk')], verbose_name='')
    created = tables.DateTimeColumn(verbose_name="Uploaded", format='d-M-Y hh:mm', accessor=A('docfile'),
                                    orderable=True)
    size = tables.Column(verbose_name="Size (kB)", accessor=A('docfile'), orderable=True)

    # def render_docfile(self,value):
    #    return value.name[2:]

    def render_created(self, value):
        # print("DEBUG: File=", value.storage.created_time(value.name))
        return value.storage.get_created_time(value.name)

    def render_size(self, value):
        return value.storage.size(value.name) / 1000

    class Meta:
        model = Document
        attrs = {"class": "ui-responsive table table-hover"}
        fields = ['id', 'docfile', 'description', 'study', 'created', 'size']
        sortable = True
        order_by_field = 'id'
