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
    docfile = models.FileField(verbose_name="Document")
    description = models.CharField(_("Description"), max_length=200, null=True, blank=True)
    doctype = models.CharField(_("Doctype"), max_length=10)
    study = models.ForeignKey("Study", on_delete=models.SET_NULL, blank=True, null=True)

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


