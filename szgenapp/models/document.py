from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from os import path

DOC_TYPES = (
    ('.csv', 'CSV'),
    ('.xls', 'Excel (xls)'),
    ('.xlsx', 'Excel (xlsx)'),
    ('.pdf', 'PDF'),
    ('.doc', 'Word DOC'),
    ('.docx', 'Word DOC (docx)'),
    ('.txt', 'Text')
)


class Document(models.Model):
    id = models.AutoField(primary_key=True)
    docfile = models.FileField(verbose_name="Document", help_text="Upload a document for storage and/or importing data")
    description = models.CharField(_("Description"), max_length=200, null=True, blank=True)
    doctype = models.CharField(_("Doctype"), max_length=10)
    study = models.ForeignKey("Study", on_delete=models.SET_NULL, blank=True, null=True,
                              help_text='Select only if document is related to one particular study')

    class Meta:
        permissions = [("can_import_data", "Can import data from CSV files")]

    def __str__(self):
        return self.docfile.name

    def getextension(self):
        if not self.docfile:
            return ''
        ext = path.splitext(self.docfile.name)[1]  # [0] returns path+filename
        return ext

    def clean(self):
        ext = self.getextension()
        valid_extensions = [x[0] for x in DOC_TYPES]
        if not ext.lower() in valid_extensions:
            print_exts = [x[1] for x in DOC_TYPES]
            raise ValidationError(u'Unsupported file type (' + ','.join(print_exts) + ').')


