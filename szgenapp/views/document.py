from django.http import HttpResponse
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView, FormView
from django_filters.views import FilterView
from django_tables2.export.views import ExportMixin
from django_tables2.views import SingleTableMixin
from django.shortcuts import render
from django.db import IntegrityError

import os
import pandas as pd

from szgenapp.filters.document import DocumentFilter
from szgenapp.forms.document import DocumentForm, ImportForm
from szgenapp.models.document import Document
from szgenapp.tables.document import DocumentTable
from szgenapp.models.participants import Participant, StudyParticipant, PARTICIPANT_STATUS_CHOICES, COUNTRY_CHOICES
from szgenapp.models.studies import Study, STATUS_CHOICES


# DOCUMENTS
class DocumentList(SingleTableMixin, ExportMixin, FilterView):
    """
    List of Documents
    """
    model = Document
    template_name = 'document/document-list.html'
    filterset_class = DocumentFilter
    table_class = DocumentTable

    def get_context_data(self, *args, **kwargs):
        context = super(DocumentList, self).get_context_data(*args, **kwargs)
        context['reset_url'] = 'documents_list'
        context['title'] = 'Documents'
        return context


class DocumentDetail(DetailView):
    """
    Information about single document
    """
    model = Document
    context_object_name = 'document'
    template_name = 'document/document-view.html'
    # raise_exception = True


class DocumentCreate(CreateView):
    """
    Create a document from uploaded file
    """
    model = Document
    template_name = 'document/document-create.html'
    form_class = DocumentForm
    success_url = reverse_lazy('documents_list')

    # raise_exception = True

    def form_valid(self, form):
        try:
            if form.is_valid():
                instance = form.save(commit=False)
                doc = form.cleaned_data['docfile']
                if doc:
                    ext = os.path.splitext(doc.name)
                    instance.doctype = ext[1]
                instance.save()
                return super(self.__class__, self).form_valid(form)
        except IntegrityError as e:
            msg = 'Database Error: Unable to create Document: %s' % e
            form.add_error('document', msg)
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse('documents_detail', args=[self.object.pk])


class DocumentUpdate(UpdateView):
    """
    Update a document details
    """
    model = Document
    form_class = DocumentForm
    template_name = 'document/document-create.html'
    success_url = reverse_lazy('documents_list')
    # raise_exception = True


class DocumentDelete(DeleteView):
    """
    Delete document
    """
    model = Document
    success_url = reverse_lazy("documents_list")
    template_name = 'document/document-confirm-delete.html'
    # raise_exception = True


class DocumentImport(FormView):
    """
    Import data from document
    1. CSV files only
    2. Headers in first line with no gaps, no spaces in headings, no commas
    3. Data cells not empty with no commas, numbers only in number columns
    4. One table per import - fields will match headings (export a table for example)
    """
    template_name = 'document/document-import.html'
    form_class = ImportForm

    def get_context_data(self, **kwargs):
        initial = super(self.__class__, self).get_context_data(**kwargs)
        initial['title'] = 'Import data from document'
        if self.kwargs.get('pk'):
            document = Document.objects.get(pk=self.kwargs.get('pk'))
            initial['document'] = document
        initial['success'] = None
        initial['error'] = None
        return initial

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            # process data import
            doc = form.cleaned_data['document']
            datatable = form.cleaned_data['datatable']
            self.data_import(doc, datatable)
            return render(request, self.template_name, {'form': form, 'success': 'Import Success'})
        return render(request, self.template_name, {'form': form, 'error': 'Failed to import'})

    def data_import(self, doc, datatable):
        print('data import:', doc.docfile.name, datatable)

        if doc and datatable:
            try:
                fname = doc.docfile.name
                ext = doc.getextension()
                if ext == '.csv':
                    df = pd.read_csv(doc.docfile.path)
                    df = df.fillna('')
                    header = list(df)
                    # Match Table to data
                    if datatable == 'Study' and 'Precursor' in header:
                        self.importStudyData(df)

                    if datatable == 'Participant' and 'Participant' in header:
                        self.importParticipantData(df)
                    else:
                        print('Error: unable to match')

                return HttpResponse("Data Uploaded from %s." % fname)
            except FileNotFoundError as e:
                msg = 'Upload failed: %s' % e
                print(msg)
                raise FileNotFoundError(msg)
            except ChildProcessError as c:
                raise ChildProcessError(c)

    def importStudyData(self, df):
        """
        Manage upload of data for Study
        :param df: Dataframe with field headers and NaN's stripped
        :return:
        """
        print('Upload for Study table')
        for index, row in df.iterrows():
            title = row['Title']
            qs = Study.objects.filter(title__iexact=title)
            if qs.count() == 0:
                precursor = row['Precursor']
                description = row['Description']
                status = row['Status']
                notes = row['Notes']
                # Create Study
                try:
                    Study.objects.create(title=title, precursor=precursor,
                                     description=description, status=status, notes=notes)
                except IntegrityError as e:
                    msg = 'Unable to create Study: %s' % e
                    print(msg)
                    raise ChildProcessError(msg)

    def importDatasetData(self, df):
        """
        Manage import of Dataset data
        :param df: Dataframe with field headers and NaN's stripped
        :return:
        """
        print('Upload for Dataset table')
        participants = [p.getFullNumber() for p in StudyParticipant.objects.all()]
        for index, row in df.iterrows():
            if row['Participant'] in participants:
                print('Participant already exists - delete first')
            else:
                print('Create Participant')
                pid = row['Participant']
                s = Study.objects.filter(code__startsWith=pid[:3])
                p = Participant.objects.create()

    def importClinicalData(self, df):
        """
        Manage import of Clinical Participant
        :param df:
        :return:
        """
        print('Upload for Participant table')
        participants = [p.getFullNumber() for p in StudyParticipant.objects.all()]
        for index, row in df.iterrows():
            if row['Participant'] in participants:
                print('Participant already exists - delete first')
            else:
                print('Create Participant')
                pid = row['Participant']
                s = Study.objects.filter(code__startsWith=pid[:3])
                p = Participant.objects.create()