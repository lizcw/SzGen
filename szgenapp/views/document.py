from django.http import HttpResponse
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView, FormView
from django_filters.views import FilterView
from django_tables2.export.views import ExportMixin
from django_tables2.views import SingleTableMixin
from django.shortcuts import render
from django.db import IntegrityError, Error, transaction

import os
import pandas as pd

from szgenapp.filters.document import DocumentFilter
from szgenapp.forms.document import DocumentForm, ImportForm
from szgenapp.models.document import Document
from szgenapp.tables.document import DocumentTable
from szgenapp.models.participants import Participant, StudyParticipant, PARTICIPANT_STATUS_CHOICES, COUNTRY_CHOICES
from szgenapp.models.studies import Study, STATUS_CHOICES
from szgenapp.models.datasets import *
from szgenapp.models.clinical import *
from szgenapp.models.samples import *
from szgenapp.validators import validate_int, validate_bool, validate_date


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

    def get_initial(self):
        initial = super(self.__class__, self).get_initial()
        initial['title'] = 'Import data from document'
        if self.kwargs.get('pk'):
            document = Document.objects.get(pk=self.kwargs.get('pk'))
            initial['document'] = document
        initial['success'] = None
        initial['error'] = None
        return initial

    # def get_context_data(self, **kwargs):
    #     initial = super(self.__class__, self).get_context_data(**kwargs)
    #     initial['title'] = 'Import data from document'
    #     if self.kwargs.get('pk'):
    #         document = Document.objects.get(pk=self.kwargs.get('pk'))
    #         initial['document'] = document
    #     initial['success'] = None
    #     initial['error'] = None
    #     return initial

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
                    elif datatable == 'Participant' and 'DIGS' in header:
                        self.importDatasetParticipantData(df)
                    elif datatable == 'Clinical' and 'PrimID' in header:
                        # second row for mapped headings
                        df = pd.read_csv(doc.docfile.path, header=1)
                        df = df.fillna('')
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
                except Error as e:
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
            except Error as e:
                msg = 'Unable to create Dataset: %s' % e
                print(msg)
                raise ChildProcessError(msg)

    def importDatasetParticipantData(self, df):
        """
        Manage import of Dataset Participant data
        :param df: Dataframe with field headers and NaN's stripped
        :return:
        """
        print('Upload for Dataset Participant table')
        for index, row in df.iterrows():
            group = row['Group']
            pid = row['ID#']
            ds = Dataset.objects.filter(group__iexact=group)
            if ds.count() <= 0 or len(group) <= 0 or len(pid) <= 0:
                print('Group not found: ', row['Group'])
            try:
                ds = ds.first()
                p = StudyParticipant.objects.filter(fullnumber__exact=pid)
                msg = 'Dataset Participant %s for %s' % (pid, group)
                if p.count() <= 0:
                    print(msg, ' - Not found')
                    continue
                elif p.count() > 1:
                    print(msg, ' - Multiple found')
                    continue
                else:
                    p = p.first()
                print(msg)
                if hasattr(row, 'Screen ID (NPID)'):
                    npid = row['Screen ID (NPID)']
                    print('setting NPID: ', npid)
                    p.participant.npid = npid
                    p.participant.save()
                dp = DatasetRow.objects.create(dataset=ds,
                                               participant=p,
                                               digs=validate_int(row['DIGS']),
                                               figs=validate_int(row['FIGS']),
                                               narrative=validate_int(row['Narrative']),
                                               records=validate_int(row['Medical Records']),
                                               consensus=validate_int(row['Consensus']),
                                               ldps=validate_int(row['LDPS']),
                                               notes=validate_int(row['Notes'])
                                               )
                print(msg, ' - Created DatasetParticipant: ', dp.id)
            except Error as e:
                msg = 'Unable to create Dataset Participant: %s' % e
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
        df = df.drop_duplicates('full number', keep='first')

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
                fnum = fullnumber[len(study.precursor) + len(district):]
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

    def importClinicalData(self, df):
        """
        Manage import of Clinical Data from FinalMaster.xls
        Replaced headers with matching fields - manual and export as csv
        Updates Participant Country, secondary id
        Loads all Clinical data
        :param df:
        :return:
        """
        print('Upload for Clinical table')
        for index, row in df.iterrows():
            participantid = row['participant']
            studyparticipants = StudyParticipant.objects.filter(fullnumber__iexact=participantid)
            if len(participantid) <= 0 or studyparticipants.count() <= 0:
                print('Participant not found or ID is blank - skipping: ', index, ' fullnumber:', participantid)
            else:
                studyparticipant = studyparticipants.first()
                # if hasattr(studyparticipant, 'clinical'):
                #     print('Participant already has clinical record - skipping: ', index, ' fullnumber:', participantid)
                #     continue
                print('Create Participant: ', index, ' fullnumber:', participantid)
                participant = studyparticipant.participant
                # Update participant fields
                participant.secondaryid = row['secondaryid']
                participant.country = row['country']
                participant.save()
                print('Participant updated: id=', participant.id, ' fullnumber:', participantid)
                # Create clinical record
                clinical = Clinical.objects.create(participant=studyparticipant)
                print('Clinical record created: ', clinical.id)
                # Create subsets

                for subclinical in CLINICAL_SUBTABLES:
                    print('create ', subclinical, ' for ', participantid)
                    sub = None
                    try:
                        if subclinical == 'demographic':
                            sub = Demographic.objects.create(clinical=clinical,
                                                             gender=row[subclinical + '-gender'],
                                                             age_assessment=validate_int(
                                                                 row[subclinical + '-age_assessment']),
                                                             marital_status=row[subclinical + '-marital_status'],
                                                             living_arr=row[subclinical + '-living_arr'],
                                                             years_school=validate_int(
                                                                 row[subclinical + '-years_school']),
                                                             current_emp_status=row[
                                                                 subclinical + '-current_emp_status'],
                                                             employment_history=validate_int(
                                                                 row[subclinical + '-employment_history']))

                        elif subclinical == 'diagnosis':
                            # Illness duration field
                            ill = row[subclinical + '-illness_duration']
                            ill_approx = ill.endswith('+')
                            if ill_approx:
                                ill = ill[:-1]

                            # dup field
                            dup = row[subclinical + '-dup']
                            dup_approx = dup.endswith('+')
                            if dup_approx:
                                dup = dup[:-1]

                            # hospitalisation field
                            hos = row[subclinical + '-hospitalisation_number']
                            hos_approx = hos.startswith('>')
                            if hos_approx:
                                hos = hos[1:]

                            sub = Diagnosis.objects.create(clinical=clinical,
                                                           summary=row[subclinical + '-summary'],
                                                           age_onset=validate_int(row[subclinical + '-age_onset']),
                                                           illness_duration=validate_int(ill),
                                                           illness_duration_approx=ill_approx,
                                                           age_first_treatment=validate_int(
                                                               row[subclinical + '-age_first_treatment']),
                                                           dup=validate_int(dup), dup_approx=dup_approx,
                                                           hospitalisation=row[subclinical + '-hospitalisation'],
                                                           hospitalisation_number=validate_int(hos),
                                                           hospitalisation_number_approx=hos_approx)
                        elif subclinical == 'medicalhistory':
                            # all string/text fields
                            fieldlist = {field.name: row[subclinical + '-' + field.name] for field in
                                         MedicalHistory._meta.fields if field.name != 'clinical'}
                            print(fieldlist)
                            sub = MedicalHistory(clinical=clinical, **fieldlist)
                            sub.save()

                        elif subclinical == 'symptomsgeneral':
                            sub = SymptomsGeneral.objects.create(clinical=clinical,
                                                                 onset=row[subclinical + '-onset'],
                                                                 severity_pattern=validate_int(
                                                                     row[subclinical + '-severity_pattern']),
                                                                 symptom_pattern=validate_int(
                                                                     row[subclinical + '-symptom_pattern']),
                                                                 illness_course=validate_int(
                                                                     row[subclinical + '-illness_course']),
                                                                 curr_gaf=row[subclinical + '-curr_gaf'],
                                                                 wl_gaf=row[subclinical + '-wl_gaf'],
                                                                 current_ap_medication=row[
                                                                     subclinical + '-current_ap_medication'],
                                                                 clozapine_status=row[
                                                                     subclinical + '-clozapine_status'],
                                                                 treatment_resistant=row[
                                                                     subclinical + '-treatment_resistant'])
                        elif subclinical == 'symptomsdelusion':
                            # all string/text fields
                            fieldlist = {field.name: row[subclinical + '-' + field.name] for field in
                                         SymptomsDelusion._meta.fields if field.name != 'clinical'}
                            print(fieldlist)
                            sub = SymptomsDelusion(clinical=clinical, **fieldlist)
                            sub.save()

                        elif subclinical == 'symptomshallucination':
                            # all string/text fields
                            fieldlist = {field.name: row[subclinical + '-' + field.name] for field in
                                         SymptomsHallucination._meta.fields if field.name != 'clinical'}
                            print(fieldlist)
                            sub = SymptomsHallucination(clinical=clinical, **fieldlist)
                            sub.save()

                        elif subclinical == 'symptomsbehaviour':
                            # all string/text fields
                            fieldlist = {field.name: row[subclinical + '-' + field.name] for field in
                                         SymptomsBehaviour._meta.fields if field.name != 'clinical'}
                            print(fieldlist)
                            sub = SymptomsBehaviour(clinical=clinical, **fieldlist)
                            sub.save()

                        elif subclinical == 'symptomsdepression':
                            # all string/text fields except one
                            fieldlist = {field.name: row[subclinical + '-' + field.name] for field in
                                         SymptomsDepression._meta.fields if
                                         field.name not in ['clinical', 'depressive_symptoms_count']}
                            print(fieldlist)
                            sub = SymptomsDepression(clinical=clinical, **fieldlist)
                            sub.depressive_symptoms_count = validate_int(
                                row[subclinical + '-depressive_symptoms_count'])
                            sub.save()

                        elif subclinical == 'symptomsmania':
                            # all string/text fields except one
                            fieldlist = {field.name: row[subclinical + '-' + field.name] for field in
                                         SymptomsMania._meta.fields if
                                         field.name not in ['clinical', 'manic_count']}
                            print(fieldlist)
                            sub = SymptomsMania(clinical=clinical, **fieldlist)
                            sub.manic_count = validate_int(row[subclinical + '-manic_count'])
                            sub.save()

                        if sub:
                            msg = 'Saved %s with ID=%d for %s' % (subclinical.upper(), sub.pk, participantid)
                            print(msg)
                    except KeyError as e:
                        msg = 'Error in parsing data for %s row: %d - %s' % (subclinical, index, e)
                        raise ChildProcessError()

    def importSampleData(self, df):
        """
        Import Samples from main table.csv (Access DB) for existing Participants only
        :param df:
        :return:
        """
        print('Upload for Sample table')
        for index, row in df.iterrows():
            fullnumber = row['full number']
            participants = StudyParticipant.objects.filter(fullnumber__exact=fullnumber)
            if len(fullnumber) <= 0 or participants.count() <= 0:
                print('Participant not found or is blank - skipping: ', row['id'], ' fullnumber:', fullnumber)
            else:
                participant = participants.first() #TODO Check what to do with multiple
                msg = 'Participant %s loaded' % fullnumber
                # print(msg)
                # SAMPLE_TYPE
                sample_type = row['plasma']
                if len(sample_type) <= 0:
                    print(msg, ' - No sample type - skipping')
                    continue
                if sample_type == 'No' and hasattr(row, 'Notes') and row['Notes'].startswith('WB'):
                    sample_type = 'WB'
                elif sample_type == 'Serum':
                    sample_type = 'SERUM'
                elif sample_type == 'Yes':
                    sample_type = 'PLASMA'

                # REBLEED
                rebleed = validate_bool(row['rebleed'])
                # ARRIVAL DATE
                arrival = validate_date(row['Arrival date'])
                # CHECK IF SAMPLE ALREADY EXISTS
                existing = Sample.objects.filter(participant=participant).filter(sample_type__exact=sample_type).filter(arrival_date=arrival)
                if existing.count() > 0:
                    print(msg, ' - existing sample found: ', existing)
                    continue
                # CREATE SAMPLE
                try:
                    with transaction.atomic():
                        sample = Sample.objects.create(participant=participant,
                                                       sample_type=sample_type,
                                                       rebleed=rebleed,
                                                       arrival_date=arrival,
                                                       notes=row['Notes'])
                        print(msg, '- SAMPLE created: ', sample.id)
                except Error as e:
                    raise e
                # CREATE HARVEST SAMPLE
                complete = validate_date(row['harvest date']) is not None
                try:
                    with transaction.atomic():
                        harvest = HarvestSample.objects.create(sample=sample,
                                                               regrow_date=validate_date(row['re-grow date']),
                                                               harvest_date=validate_date(row['harvest date']),
                                                               complete=complete,
                                                               notes=row['harvest notes'])
                        print(msg, '- HARVEST created: ', harvest.id)
                except Error as e:
                    raise e

                # TRANSFORM SAMPLE
                transform_date = validate_date(row['T-date'])
                if transform_date is not None:
                    try:
                        with transaction.atomic():
                            transform = TransformSample.objects.create(sample=sample,
                                                                       transform_date=transform_date,
                                                                       failed=validate_bool(row['T-failed']),
                                                                       notes=row['Transform Notes']
                                                                       )
                            print(msg, '- TRANSFORM created: ', transform.id)
                    except Error as e:
                        raise e

                # SHIPMENT
                shipment_date = validate_date(row['Shipment Date'])
                if shipment_date is not None:
                    try:
                        with transaction.atomic():
                            shipment = Shipment.objects.create(sample=sample,
                                                               shipment_date=shipment_date,
                                                               reference=row['Reference No'],
                                                               rutgers_number=row['Rutgers No'],
                                                               notes=row['Shipment Notes']
                                                               )
                            print(msg, '- SHIPMENT created: ', shipment.id)
                    except Error as e:
                        raise e

                # SUBSAMPLE - LCYTES
                try:
                    with transaction.atomic():
                        # Create 3 locations = 3 subsamples
                        for loc in range(1,4):
                            location = row['lcyte loc ' + str(loc)]
                            notes = ''
                            if location is None or location == '':
                                continue
                            if location == 'O' or location == 0:
                                used = True
                                location_obj=None
                            else:
                                used = False
                                parts = location.split('/')
                                if len(parts) == 3:
                                    location_obj = Location.objects.create(tank=parts[0], shelf=parts[1], cell=parts[2])
                                else:
                                    notes = 'Location: ' + location
                                    location_obj = None
                            lcl = SubSample.objects.create(sample=sample,
                                                           sample_num=loc,
                                                           sample_type='LCYTE',
                                                           storage_date=validate_date(row['Storage date']),
                                                           used=used,
                                                           location=location_obj,
                                                           notes=notes)
                            print(msg, '- SUBSAMPLE LCYTE created: ', lcl.id)
                except Error as e:
                    raise e

                # SUBSAMPLE - LCL
                try:
                    with transaction.atomic():
                        # Create 5 locations = 5 subsamples
                        for loc in range(1, 6):
                            location = row['LCL Location ' + str(loc)]
                            notes = ''
                            if location is None or location == '':
                                continue
                            if location == 'O' or location == 0:
                                used = True
                                location_obj = None
                            else:
                                used = False
                                parts = location.split('/')
                                print('location: ', location)
                                if len(parts) == 3:
                                    location_obj = Location.objects.create(tank=parts[0], shelf=parts[1], cell=parts[2])
                                else:
                                    notes = 'Location: ' + location
                                    location_obj = None
                            lcl = SubSample.objects.create(sample=sample,
                                                           sample_num=loc,
                                                           sample_type='LCL',
                                                           storage_date=validate_date(row['LCL storage date']),
                                                           used=used,
                                                           location=location_obj,
                                                           notes=notes)
                            print(msg, '- SUBSAMPLE LCL created: ', lcl.id)
                except Error as e:
                    raise e

                # SUBSAMPLE - DNA
                try:
                    with transaction.atomic():
                        # No location
                        notes = row['DNA Notes']
                        extraction_date = validate_date(row['DNA Extraction Date'])
                        if notes.find('DNA') > 0 and extraction_date is not None:
                            dna = SubSample.objects.create(sample=sample,
                                                           sample_num=1,
                                                           sample_type='DNA',
                                                           storage_date=validate_date(row['Storage date']),
                                                           extraction_date=extraction_date,
                                                           notes=notes)
                            print(msg, '- SUBSAMPLE DNA created: ', dna.id)
                except Error as e:
                    raise e
