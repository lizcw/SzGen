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
from szgenapp.models.datasets import *


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
            msg = 'Data imported Successfully from %s to %s' % (doc.docfile.name, datatable)
            print(msg)
            return render(request, self.template_name, {'form': form, 'success': msg})
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
                    elif datatable == 'Dataset' and 'Filetype' in header:
                        self.importDatasetData(df)
                    elif datatable == 'Clinical' and 'Filetype' in header:
                        self.importClinicalData(df)
                    elif datatable == 'Participant' and 'alpha' in header:
                        # Load participants only (subset)
                        self.importParticipantData(df)
                    elif datatable == 'Sample' and 'alpha' in header:
                        # Load samples only (subset)
                        self.importSampleData(df)
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
        for index, row in df.iterrows():
            if DatasetFile.objects.filter(dataset__group=row['Group']).filter(location=row['Location']).filter(
                    type=row['Type']).count() > 0:
                print('DatasetFile already exists: ', row)
                continue
            try:
                group = row['Group']
                ds = Dataset.objects.filter(group__iexact=group)
                if ds.count() == 0:
                    print('Create Dataset Group first')
                    ds = Dataset.objects.create(group=group)
                else:
                    ds = ds.first()
                print('Create Dataset File')
                DatasetFile.objects.create(dataset=ds, type=row['Type'], location=row['Location'],
                                           filetype=row['Filetype'])
            except IntegrityError as e:
                msg = 'Unable to create Dataset: %s' % e
                print(msg)
                raise ChildProcessError(msg)

    def importParticipantData(self, df):
        """
        Manage import of Participant data from Sample Access DB
        Only participant columns used: id, Study, alpha, full number
        Mandatory fields:
            country - default as India - change with clinical data
            status - set as active
        :param df: Loaded dataframe
        :return:
        """
        print('Upload for Participant table')
        # Load participant once only
        df.drop_duplicates('full number', keep='first', inplace=True)
        # participants = [p.getFullNumber() for p in StudyParticipant.objects.all()]
        for index, row in df.iterrows():
            fullnumber = row['full number']
            participants = StudyParticipant.objects.filter(fullnumber__exact=fullnumber)
            if len(fullnumber) <= 0 or participants.count() > 0:
                print('Participant already exists or is blank - skipping: ', row['id'], ' fullnumber:', fullnumber)
            else:
                print('Create Participant: ', row['id'], ' fullnumber:', fullnumber)
                study = row['Study']
                alpha = row['alpha']
                sid = row['id']
                studies = Study.objects.filter(title__iexact=study)
                if studies.count() == 0:
                    print('Study not found: ', study, ' rowid:', row['id'])
                    continue

                study = studies[0]

                # Parse for district number
                if fullnumber.startswith('CBZ'):
                    district = fullnumber[3:4]
                else:
                    district = ''
                # Parse for family-individual - strip off precursor
                fnum = fullnumber[len(study.precursor)+len(district):]
                idparts = fnum.split('-')
                if len(idparts) >= 2:
                    individual = idparts[-1]
                    family = idparts[-2]
                else:
                    individual = ''
                    family = ''
                try:
                    p = Participant.objects.create(status='ACTIVE', country='INDIA', alphacode=alpha, accessid=sid)
                    sp = StudyParticipant.objects.create(participant=p, study=study, fullnumber=fullnumber,
                                                         district=district, family=family, individual=individual)
                except IntegrityError as e:
                    msg = 'Error creating Participant and StudyParticipant: rowid: %s - %s' % (sid, e)
                    print(msg)
                    raise ChildProcessError(msg)
