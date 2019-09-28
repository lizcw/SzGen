import logging
import os

import pandas as pd
from django.db import IntegrityError, Error, transaction
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView, FormView
from django_filters.views import FilterView
from django_tables2.export.views import ExportMixin
from django_tables2.views import SingleTableMixin
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from szgenapp.filters.document import DocumentFilter
from szgenapp.forms.document import DocumentForm, ImportForm
from szgenapp.models.clinical import *
from szgenapp.models.datasets import *
from szgenapp.models.document import Document
from szgenapp.models.participants import StudyParticipant, COUNTRY_CHOICES
from szgenapp.models.samples import *
from szgenapp.models.studies import Study
from szgenapp.tables.document import DocumentTable
from szgenapp.validators import validate_int, validate_bool, validate_date, convert_Nil

logger = logging.getLogger(__name__)

# DOCUMENTS
class DocumentList(LoginRequiredMixin, SingleTableMixin, ExportMixin, FilterView):
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


class DocumentDetail(LoginRequiredMixin, DetailView):
    """
    Information about single document
    """
    model = Document
    context_object_name = 'document'
    template_name = 'document/document-view.html'


class DocumentCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """
    Create a document from uploaded file
    """
    model = Document
    template_name = 'document/document-create.html'
    form_class = DocumentForm
    success_url = reverse_lazy('documents_list')
    permission_required = 'szgenapp.add_document'

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
            form.add_error(None, msg)
            logger.error(msg)
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse('documents_detail', args=[self.object.pk])


class DocumentUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """
    Update a document details
    """
    model = Document
    form_class = DocumentForm
    template_name = 'document/document-create.html'
    success_url = reverse_lazy('documents_list')
    permission_required = 'szgenapp.change_document'


class DocumentDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """
    Delete document
    """
    model = Document
    success_url = reverse_lazy("documents_list")
    template_name = 'document/document-confirm-delete.html'
    permission_required = 'szgenapp.delete_document'


class DocumentImport(LoginRequiredMixin, PermissionRequiredMixin, FormView):
    """
    Import data from document
    1. CSV files only
    2. Headers in first line with no commas
    3. Data cells not empty with no commas, numbers only in number columns
    4. One table per import - fields will match headings
    """
    template_name = 'document/document-import.html'
    form_class = ImportForm
    permission_required = 'can_import_data'

    def get_initial(self):
        initial = super(self.__class__, self).get_initial()
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
            logger.info(msg)
            return render(request, self.template_name, {'form': form, 'success': msg})
        return render(request, self.template_name, {'form': form, 'error': 'Failed to import'})

    def data_import(self, doc, datatable):
        fmsg = 'Data import: %s to %s ' % (doc.docfile.name, datatable)
        errmsg = ''
        if doc and datatable:
            try:
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
                        errmsg = '- Error: unable to match data headers to table headers'
                        logger.error(errmsg)
                msg = "%s %s" % (fmsg, errmsg)
                return HttpResponse(msg)
            except FileNotFoundError as e:
                msg = "%s - %s" % (fmsg, e)
                logger.error(msg)
                raise FileNotFoundError(msg)
            except ChildProcessError as c:
                msg = "%s - %s" % (fmsg, c)
                logger.error(msg)
                raise ChildProcessError(c)

    def importStudyData(self, df):
        """
        Manage upload of data for Study
        :param df: Dataframe with field headers and NaN's stripped
        :return:
        """
        fmsg = 'IMPORT Study table data'
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
                    study = Study.objects.create(title=title, precursor=precursor,
                                         description=description, status=status, notes=notes)
                    msg = "%s - CREATED %s" % (fmsg, study.title)
                    logger.debug(msg)
                except Error as e:
                    msg = "%s - %s" % (fmsg, e)
                    logger.error(msg)
                    raise ChildProcessError(msg)
            else:
                msg = "%s - Exists - SKIPPED [Row %d] %s" % (fmsg, index, title)
                logger.debug(msg)

    def importDatasetData(self, df):
        """
        Manage import of Dataset data
        :param df: Dataframe with field headers and NaN's stripped
        :return:
        """
        fmsg = 'IMPORT Dataset table data'
        for index, row in df.iterrows():
            if DatasetFile.objects.filter(dataset__group=row['Group']).filter(location=row['Location']).filter(
                    type=row['Type']).count() > 0:
                msg = "%s - Exists - SKIPPED %s" % (fmsg, str(index))
                logger.debug(msg)
                continue
            try:
                group = row['Group']
                ds = Dataset.objects.filter(group__iexact=group)
                msg = "%s - %s: %s" % (fmsg, 'Created dataset group', group)
                logger.debug(msg)
                if ds.count() == 0:
                    ds = Dataset.objects.create(group=group)
                else:
                    ds = ds.first()
                dsfile = DatasetFile.objects.create(dataset=ds, type=row['Type'], location=row['Location'],
                                           filetype=row['Filetype'])
                msg = "%s - %s: %d" % (fmsg, 'Created dataset file', dsfile.id)
                logger.debug(msg)
            except Error as e:
                msg = '%s - Unable to create Dataset: [Row %d] %s' % (fmsg, index, e)
                logger.error(msg)
                raise ChildProcessError(msg)

    def importDatasetParticipantData(self, df):
        """
        Manage import of Dataset Participant data
        Expects Dataset group to exist
        :param df: Dataframe with field headers and NaN's stripped
        :return:
        """
        fmsg = 'IMPORT Dataset Participant table data'
        for index, row in df.iterrows():
            group = row['Group']
            pid = row['ID#']
            ds = Dataset.objects.filter(group__iexact=group)
            if ds.count() <= 0 or len(group) <= 0 or len(pid) <= 0:
                msg = "%s - %s: [Row %d] %s" % (fmsg, 'Dataset Group not found - Skipping', index, group)
                logger.error(msg)
                continue
            try:
                ds = ds.first()
                p = StudyParticipant.objects.filter(fullnumber__exact=pid)
                if p.count() <= 0:
                    msg = "%s - %s: [Row %d] %s" % (fmsg, 'StudyParticipant not found - Skipping', index, pid)
                    logger.error(msg)
                    continue
                elif p.count() > 1:
                    msg = "%s - %s: [Row %d] %s" % (fmsg, 'Multiple StudyParticipants found - Skipping', index, pid)
                    logger.error(msg)
                    continue
                else:
                    p = p.first()
                # Check for NPID columns - would be better to rename data column - oh well
                npid = None
                if hasattr(row, 'Screen ID (NPID)'):
                    npid = row['Screen ID (NPID)']
                if hasattr(row, 'Screen ID'):
                    npid = row['Screen ID']
                if hasattr(row, 'NPID'):
                    npid = row['NPID']
                if npid is not None:
                    p.participant.npid = npid
                    p.participant.save()
                    msg = "%s - %s: [Row %d] %s (NPID=%s)" % (fmsg, 'Participant updated NPID', index, pid, str(npid))
                    logger.info(msg)
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
                msg = "%s - %s: [Row %d] %s" % (fmsg, 'CREATED DatasetParticipant', index, str(dp.id))
                logger.debug(msg)
            except Error as e:
                msg = "%s - %s: [Row %d] %s" % (fmsg, 'Unable to create Dataset Participant', index, e)
                logger.error(msg)
                raise ChildProcessError(msg)

    def importParticipantData(self, df):
        """
        Manage import of Participant data from Sample Access DB
        Only participant columns used: id, Study, alpha, full number
        Mandatory fields:
            country - default as Unknown - change with clinical data
            status - set as active
        :param df: Loaded dataframe
        :return:
        """
        fmsg = 'IMPORT Participant table data'
        # Load participant once only
        df = df.drop_duplicates('full number', keep='first')

        for index, row in df.iterrows():
            fullnumber = row['full number'].strip()
            studyparticipants = StudyParticipant.objects.filter(fullnumber__exact=fullnumber)
            if len(fullnumber) <= 0 or studyparticipants.count() > 0:
                msg = "%s - %s: [Row %d] %s" % (fmsg, 'StudyParticipant EXISTS or Full number is blank - Skipping',
                                                index, fullnumber)
                logger.debug(msg)
                continue
            else:
                study = row['Study'].strip().replace('-', ' ')
                alpha = row['alpha'].strip()
                sid = row['id']
                # Incorrect entry in Access DB
                if study == 'Cadence CoME':
                    study = 'Cadence CoMet'
                studies = Study.objects.filter(title__iexact=study)
                if studies.count() == 0:
                    msg = "%s - %s: [Row %d] %s" % (fmsg, 'Study not found - Skipping', index, study)
                    logger.error(msg)
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
                    sp = StudyParticipant.objects.create(status='ACTIVE', country='UNK', alphacode=alpha, accessid=sid,
                                                         study=study, fullnumber=fullnumber,
                                                         district=district, family=family, individual=individual)
                    msg = "%s - %s: [Row %d] %d fullnumber:%s" % (fmsg, 'StudyParticipant CREATED', index, sp.id, fullnumber)
                    logger.debug(msg)

                except IntegrityError as e:
                    msg = "%s - %s: [Row %d] %s" % (fmsg, 'Unable to create Participant', index, e)
                    logger.error(msg)
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
        fmsg = 'IMPORT Clinical table data'
        for index, row in df.iterrows():
            participantid = row['participant']
            studyparticipants = StudyParticipant.objects.filter(fullnumber__iexact=participantid)
            if len(participantid) <= 0 or studyparticipants.count() <= 0:
                msg = "%s - %s: [Row %d] %s" % (fmsg, 'StudyParticipant NOT FOUND or Full number is blank - Skipping',
                                                index, participantid)
                logger.error(msg)
                continue
            else:
                studyparticipant = studyparticipants.first()
                if hasattr(studyparticipant, 'clinical') and hasattr(studyparticipant.clinical, 'id'):
                    msg = "%s - %s: [Row %d] %s clinicalID=%d" % (
                    fmsg, 'StudyParticipant already has clinical record. Delete this first then rerun import - Skipping',
                    index, participantid, studyparticipant.clinical.id)
                    logger.error(msg)
                    continue
                # Update participant fields
                try:
                    participant = studyparticipant
                    if len(row['secondaryid']) > 0:
                        participant.secondaryid = row['secondaryid'].strip()
                    # Country validate
                    row_country = row['country'].strip().upper()
                    country = [x for x in COUNTRY_CHOICES if x[0] == row_country]
                    participant.country = country[0][0]
                    participant.save()
                    msg = "%s - %s: [Row %d] %d fullnumber:%s country:%s" % (
                        fmsg, 'Participant UPDATED', index, participant.id, participant.fullnumber, participant.country)
                    logger.debug(msg)
                except Error as e:
                    msg = "%s - %s: [Row %d] %s" % (fmsg, 'Unable to update Participant', index, e)
                    logger.error(msg)
                # Create clinical record
                try:
                    clinical = Clinical.objects.create(participant=studyparticipant)
                    msg = "%s - %s: [Row %d] %d fullnumber:%s" % (fmsg, 'Clinical CREATED', index,
                                                                  clinical.id, participantid)
                    logger.debug(msg)
                except Error as e:
                    msg = "%s - %s: [Row %d] %s" % (fmsg, 'Unable to create Clinical - skipping', index, e)
                    logger.error(msg)
                    continue
                # Create subclinical
                for subclinical in CLINICAL_SUBTABLES:
                    sub = None
                    if subclinical == 'demographic':
                        try:
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

                        except Error as e:
                            msg = "%s - %s %s: [Row %d] %s" % (fmsg, 'SKIPPING - Unable to create Clinical',
                                                            subclinical.upper(), index, e)
                            logger.error(msg)
                            continue

                    elif subclinical == 'diagnosis':
                        try:
                            # Illness duration field
                            ill = row[subclinical + '-illness_duration'].strip()
                            ill_approx = '+' in ill
                            if ill_approx:
                                ill = ill[:-1]

                            # dup field
                            dup = row[subclinical + '-dup'].strip()
                            dup_approx = '+' in dup
                            if dup_approx:
                                dup = dup[:-1]

                            # hospitalisation field
                            hos = row[subclinical + '-hospitalisation_number'].strip()
                            hos_approx = '>' in hos
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

                        except Error as e:
                            msg = "%s - %s %s: [Row %d] %s" % (fmsg, 'SKIPPING - Unable to create Clinical',
                                                               subclinical.upper(), index, e)
                            logger.error(msg)
                            continue
                    elif subclinical == 'medicalhistory':
                        try:
                            # all string/text fields
                            fieldlist = {field.name: row[subclinical + '-' + field.name] for field in
                                         MedicalHistory._meta.fields if field.name != 'clinical'}
                            sub = MedicalHistory(clinical=clinical, **fieldlist)
                            sub.save()

                        except Error as e:
                            msg = "%s - %s %s: [Row %d] %s" % (fmsg, 'SKIPPING - Unable to create Clinical',
                                                               subclinical.upper(), index, e)
                            logger.error(msg)
                            continue

                    elif subclinical == 'symptomsgeneral':
                        try:
                            sub = SymptomsGeneral.objects.create(clinical=clinical,
                                                                 onset=row[subclinical + '-onset'],
                                                                 severity_pattern=validate_int(
                                                                     row[subclinical + '-severity_pattern']),
                                                                 symptom_pattern=validate_int(
                                                                     row[subclinical + '-symptom_pattern']),
                                                                 illness_course=validate_int(
                                                                     row[subclinical + '-illness_course']),
                                                                 curr_gaf=convert_Nil(row[subclinical + '-curr_gaf']),
                                                                 wl_gaf=row[subclinical + '-wl_gaf'],
                                                                 current_ap_medication=row[
                                                                     subclinical + '-current_ap_medication'],
                                                                 clozapine_status=row[
                                                                     subclinical + '-clozapine_status'],
                                                                 treatment_resistant=row[
                                                                     subclinical + '-treatment_resistant'])

                        except Error as e:
                            msg = "%s - %s %s: [Row %d] %s" % (fmsg, 'SKIPPING - Unable to create Clinical',
                                                               subclinical.upper(), index, e)
                            logger.error(msg)
                            continue
                    elif subclinical == 'symptomsdelusion':
                        try:
                            # all string/text fields
                            fieldlist = {field.name: convert_Nil(row[subclinical + '-' + field.name]) for field in
                                         SymptomsDelusion._meta.fields if field.name != 'clinical'}
                            sub = SymptomsDelusion(clinical=clinical, **fieldlist)
                            sub.save()

                        except Error as e:
                            msg = "%s - %s %s: [Row %d] %s" % (fmsg, 'SKIPPING - Unable to create Clinical',
                                                               subclinical.upper(), index, e)
                            logger.error(msg)
                            continue

                    elif subclinical == 'symptomshallucination':
                        try:
                            # all string/text fields
                            fieldlist = {field.name: convert_Nil(row[subclinical + '-' + field.name]) for field in
                                         SymptomsHallucination._meta.fields if field.name != 'clinical'}
                            sub = SymptomsHallucination(clinical=clinical, **fieldlist)
                            sub.save()

                        except Error as e:
                            msg = "%s - %s %s: [Row %d] %s" % (fmsg, 'SKIPPING - Unable to create Clinical',
                                                               subclinical.upper(), index, e)
                            logger.error(msg)
                            continue

                    elif subclinical == 'symptomsbehaviour':
                        try:
                            # all string/text fields
                            fieldlist = {field.name: convert_Nil(row[subclinical + '-' + field.name]) for field in
                                         SymptomsBehaviour._meta.fields if field.name != 'clinical'}
                            sub = SymptomsBehaviour(clinical=clinical, **fieldlist)
                            sub.save()

                        except Error as e:
                            msg = "%s - %s %s: [Row %d] %s" % (fmsg, 'SKIPPING - Unable to create Clinical',
                                                               subclinical.upper(), index, e)
                            logger.error(msg)
                            continue

                    elif subclinical == 'symptomsdepression':
                        try:
                            # all string/text fields except one
                            fieldlist = {field.name: row[subclinical + '-' + field.name] for field in
                                         SymptomsDepression._meta.fields if
                                         field.name not in ['clinical', 'depressive_symptoms_count']}
                            sub = SymptomsDepression(clinical=clinical, **fieldlist)
                            sub.depressive_symptoms_count = validate_int(
                                row[subclinical + '-depressive_symptoms_count'])
                            sub.save()

                        except Error as e:
                            msg = "%s - %s %s: [Row %d] %s" % (fmsg, 'SKIPPING - Unable to create Clinical',
                                                               subclinical.upper(), index, e)
                            logger.error(msg)
                            continue

                    elif subclinical == 'symptomsmania':
                        try:
                            # all string/text fields except one
                            fieldlist = {field.name: row[subclinical + '-' + field.name] for field in
                                         SymptomsMania._meta.fields if
                                         field.name not in ['clinical', 'manic_count']}
                            sub = SymptomsMania(clinical=clinical, **fieldlist)
                            sub.manic_count = validate_int(row[subclinical + '-manic_count'])
                            sub.save()

                        except Error as e:
                            msg = "%s - %s %s: [Row %d] %s" % (fmsg, 'SKIPPING - Unable to create Clinical',
                                                               subclinical.upper(), index, e)
                            logger.error(msg)
                            continue

                    if sub:
                        msg = "%s - %s %s: [Row %d] %d clinical:%d, fullnumber:%s" % (fmsg,
                                                                                      'CREATED Clinical',
                                                                                      subclinical.upper(),
                                                                                      index, sub.pk,
                                                                                      clinical.id, participantid)
                        logger.debug(msg)


    def importSampleData(self, df):
        """
        Import Samples from main table.csv (Access DB) for existing Participants only
        :param df:
        :return:
        """
        fmsg = 'IMPORT Sample table data'
        for index, row in df.iterrows():
            fullnumber = row['full number'].strip()
            sample = None  #INITIALISE
            participants = StudyParticipant.objects.filter(fullnumber__exact=fullnumber)
            if len(fullnumber) <= 0 or participants.count() <= 0:
                msg = "%s - %s: [Row %d] ID=%s Fullnumber=%s" % (fmsg, 'StudyParticipant NOT FOUND or Full number is blank - Skipping',
                                                index, row['id'], fullnumber)
                logger.error(msg)
                continue
            else:
                participant = participants.first()
                # SAMPLE_TYPE
                sample_types = []
                plasma = row['plasma'].strip()
                notes = row['Notes'].strip()
                wb = row['WB']  # Highly inconsistent data field
                if wb not in ['No', 'No?', 'no', 0, ''] or notes == 'WB DNA ONLY':
                    sample_types.append('WB')
                if len(sample_types) <= 0 and (plasma is None or len(plasma) <= 0):
                    sample_types.append('UNKNOWN')
                    msg = "%s - %s: [Row %d] %s" % (fmsg, 'Sample TYPE NOT FOUND - setting Unknown', index, fullnumber)
                    logger.error(msg)
                else:
                    if plasma == 'Yes':
                        sample_types.append('PLASMA')
                    elif plasma == 'Serum':
                        sample_types.append('SERUM')
                    if 'SALIVA' in notes.upper():
                        sample_types.append('SALIVA')
                    if 'PAXGENE' in notes.upper() and 'NO PAXGENE' not in notes.upper():
                        # Note there is No Paxgene in notes but not with 'plasma'=No
                        sample_types.append('PAXGENE')
                if len(sample_types) <= 0:
                    sample_types.append('UNKNOWN')
                    msg = "%s - %s: [Row %d] %s" % (fmsg, 'Sample TYPE CAN NOT BE UNDERSTOOD - setting Unknown', index, fullnumber)
                    logger.error(msg)

                stypes = SampleType.objects.filter(name__in=sample_types)
                # Check SampleType exists (should be set up by Admin) otherwise create based on SAMPLE_TYPES
                if stypes.count() == 0:
                    types = [x for x in SAMPLE_TYPES if x[0] in sample_types]
                    for type in types:
                        s, created = SampleType.objects.get_or_create(name=type[0])
                        if created:
                            msg = "%s - %s: [Row %d] %s" % (fmsg, 'Sample TYPE created', index, s)
                            logger.info(msg)
                    stypes = SampleType.objects.filter(name__in=sample_types)

                # REBLEED
                rebleed = validate_bool(row['rebleed'])
                # ARRIVAL DATE
                arrival = validate_date(row['Arrival date'])
                # CHECK IF SAMPLE ALREADY EXISTS - DUPLICATED
                existing = Sample.objects.filter(participant=participant).filter(arrival_date=arrival).filter(rebleed=rebleed)
                duplicate = existing.count() > 0
                if duplicate:
                    # Append access id if different otherwise assume re-run and just skip (DEBUG)
                    if str(row['id']) in participant.accessid:
                        msg = "%s - %s: [Row %d] %s SampleId=%d already loaded" % (
                            fmsg, 'Sample LOADED - Skipping', index, fullnumber, existing[0].pk)
                        logger.debug(msg)
                        continue
                    else:
                        # Try and load sample in duplicate
                        accessid = "%s, %s" % (participant.accessid, row['id'])
                        participant.accessid = accessid
                        participant.save()
                        msg = "%s - %s: [Row %d] %s existingSampleId=%d AccessID=%s existingAccessID=%s" % (
                            fmsg, 'Sample DUPLICATE - Access ID appended', index, fullnumber, existing[0].pk, participant.accessid,
                            row['id'])
                        logger.error(msg)
                        # USE EXISTING SAMPLE (SHOULD ONLY BE ONE)
                        sample = existing.first()

                # CREATE NEW SAMPLE
                else:
                    try:
                        with transaction.atomic():
                            sample = Sample.objects.create(participant=participant,
                                                           rebleed=rebleed,
                                                           arrival_date=arrival,
                                                           notes=row['Notes'])
                            msg = "%s - %s: [Row %d] %s sampleid=%d" % (fmsg, 'Sample CREATED',
                                                                        index, fullnumber, sample.pk)
                            for stype in stypes:
                                sample.sample_types.add(stype)
                                msg += ' sample_type=%s' % stype.name
                            sample.save()
                            logger.debug(msg)
                    except Error as e:
                        msg = "%s - %s: [Row %d] %s : %s" % (fmsg, 'Error: Sample could not be created',
                                                        index, fullnumber, e)
                        logger.error(msg)
                if sample is None:
                    continue
                # CREATE HARVEST SAMPLE
                harvest_date = validate_date(row['harvest date'])
                regrow_date = validate_date(row['re-grow date'])
                notes = row['harvest notes']
                harvests = sample.harvest.filter(harvest_date=harvest_date).filter(regrow_date=regrow_date).filter(notes=notes)
                if harvests.count() == 0 and (harvest_date is not None or regrow_date is not None or len(notes) > 0):
                    complete = harvest_date is not None
                    try:
                        with transaction.atomic():
                            harvest = HarvestSample.objects.create(sample=sample,
                                                                   regrow_date=regrow_date,
                                                                   harvest_date=harvest_date,
                                                                   complete=complete,
                                                                   notes=notes)
                            msg = "%s - %s: [Row %d] %s harvestid=%d" % (fmsg, 'Sample HARVEST CREATED',
                                                                        index, fullnumber, harvest.pk)
                            logger.debug(msg)
                    except Error as e:
                        msg = "%s - %s: [Row %d] %s : %s" % (fmsg, 'Error: Sample HARVEST could not be created',
                                                             index, fullnumber, e)
                        logger.error(msg)

                # TRANSFORM SAMPLE
                transform_date = validate_date(row['T-date'])
                tdates = sample.transform.filter(transform_date=transform_date) \
                    .filter(failed=validate_bool(row['T-failed']))
                if transform_date is not None and tdates.count() == 0:
                    try:
                        with transaction.atomic():
                            transform = TransformSample.objects.create(sample=sample,
                                                                       transform_date=transform_date,
                                                                       failed=validate_bool(row['T-failed']),
                                                                       notes=row['Transform Notes']
                                                                       )
                            msg = "%s - %s: [Row %d] %s transform=%d" % (fmsg, 'Sample Transform CREATED',
                                                                         index, fullnumber, transform.pk)
                            logger.debug(msg)
                    except Error as e:
                        msg = "%s - %s: [Row %d] %s : %s" % (fmsg, 'Error: Sample Transform could not be created',
                                                             index, fullnumber, e)
                        logger.error(msg)

                # SHIPMENT
                shipment_date = validate_date(row['Shipment Date'])
                sdates = sample.shipment.filter(shipment_date=shipment_date) \
                    .filter(reference=row['Reference No']).filter(rutgers_number=row['Rutgers No'])
                if shipment_date is not None and sdates.count() == 0:
                    try:
                        with transaction.atomic():
                            shipment = Shipment.objects.create(sample=sample,
                                                               shipment_date=shipment_date,
                                                               reference=row['Reference No'],
                                                               rutgers_number=row['Rutgers No'],
                                                               notes=row['Shipment Notes']
                                                               )
                        msg = "%s - %s: [Row %d] %s shipment=%d" % (fmsg, 'Sample SHIPMENT CREATED',
                                                                 index, fullnumber, shipment.pk)
                        logger.debug(msg)
                    except Error as e:
                        msg = "%s - %s: [Row %d] %s : %s" % (fmsg, 'Error: Sample SHIPMENT could not be created',
                                                     index, fullnumber, e)
                        logger.error(msg)

                # SUBSAMPLE - LCYTES
                with transaction.atomic():
                    # Create 3 locations = 3 subsamples
                    try:
                        for loc in range(1,4):
                            location = row['lcyte loc ' + str(loc)].strip()
                            notes = ''
                            duplicates = sample.subsample_set.filter(sample_num=loc).filter(sample_type='LCYTE')\
                                .filter(storage_date=validate_date(row['Storage date']))
                            if location is None or location == '':
                                continue
                            if location in ['o', 'O', '0', 0]:
                                used = True
                                location_obj = None
                                duplicate = duplicates.filter(used=True).count() > 0
                                if duplicate:
                                    continue
                            else:
                                used = False
                                parts = location.split('/')
                                if len(parts) == 3:
                                    duplicate = duplicates.filter(location__tank=parts[0])\
                                        .filter(location__shelf=parts[1]).filter(location__cell=parts[2]).count() > 0
                                    if duplicate:
                                        continue
                                    location_obj = Location.objects.create(tank=parts[0], shelf=parts[1], cell=parts[2])

                                else:
                                    notes = 'Location could not be parsed during import: ' + location
                                    location_obj = None
                                    duplicate = duplicates.filter(notes=notes).count() > 0
                                    if duplicate:
                                        continue
                            lcl = SubSample.objects.create(sample=sample,
                                                           sample_num=loc,
                                                           sample_type='LCYTE',
                                                           storage_date=validate_date(row['Storage date']),
                                                           used=used,
                                                           location=location_obj,
                                                           notes=notes)
                            msg = "%s - %s: [Row %d] %s id=%d" % (fmsg, 'SUBSAMPLE LCYTE CREATED',
                                                                        index, fullnumber, lcl.pk)
                            logger.debug(msg)
                    except Error as e:
                        msg = "%s - %s: [Row %d] %s: %s" % (fmsg, 'Error: SUBSAMPLE LCYTE could not be created',
                                                             index, fullnumber, e)
                        logger.error(msg)

                # SUBSAMPLE - LCL
                with transaction.atomic():
                    try:
                        # Create 5 locations = 5 subsamples
                        storage_date = validate_date(row['LCL storage date'])
                        for loc in range(1, 6):
                            location = row['LCL Location ' + str(loc)]
                            notes = ''
                            duplicates = sample.subsample_set.filter(sample_num=loc).filter(sample_type='LCL')\
                                .filter(storage_date=storage_date)
                            if location is None or location == '':
                                continue
                            if location == 'O' or location == 0:
                                used = True
                                location_obj = None
                                duplicate = duplicates.filter(used=True).count() > 0
                                if duplicate:
                                    continue
                            else:
                                used = False
                                parts = location.split('/')
                                if len(parts) == 3:
                                    duplicate = duplicates.filter(location__tank=parts[0]) \
                                                    .filter(location__shelf=parts[1]).filter(
                                        location__cell=parts[2]).count() > 0
                                    if duplicate:
                                        continue
                                    location_obj = Location.objects.create(tank=parts[0], shelf=parts[1], cell=parts[2])
                                else:
                                    notes = 'Location could not be parsed during import: ' + location
                                    location_obj = None
                                    duplicate = duplicates.filter(notes=notes).count() > 0
                                    if duplicate:
                                        continue
                            lcl = SubSample.objects.create(sample=sample,
                                                           sample_num=loc,
                                                           sample_type='LCL',
                                                           storage_date=storage_date,
                                                           used=used,
                                                           location=location_obj,
                                                           notes=notes)
                            msg = "%s - %s: [Row %d] %s id=%d" % (fmsg, 'SUBSAMPLE LCL CREATED',
                                                                  index, fullnumber, lcl.pk)
                            logger.debug(msg)
                    except Error as e:
                        msg = "%s - %s: [Row %d] %s: %s" % (fmsg, 'Error: SUBSAMPLE LCL could not be created',
                                                            index, fullnumber, e)
                        logger.error(msg)

                # SUBSAMPLE - DNA
                with transaction.atomic():
                    try:
                        # No location
                        notes = row['DNA Notes']
                        extraction_date = validate_date(row['DNA Extraction Date'])
                        storage_date = validate_date(row['Storage date'])
                        if extraction_date is not None:
                            duplicates = sample.subsample_set.filter(sample_type='DNA') \
                                .filter(storage_date=storage_date)\
                                .filter(extraction_date=extraction_date)\
                                .filter(notes=notes)
                            if duplicates.count() == 0:
                                dna = SubSample.objects.create(sample=sample,
                                                               sample_num=1,
                                                               sample_type='DNA',
                                                               storage_date=storage_date,
                                                               extraction_date=extraction_date,
                                                               notes=notes)
                                msg = "%s - %s: [Row %d] %s id=%d" % (fmsg, 'SUBSAMPLE DNA CREATED',
                                                                  index, fullnumber, dna.pk)
                                logger.debug(msg)
                    except Error as e:
                        msg = "%s - %s: [Row %d] %s: %s" % (fmsg, 'Error: SUBSAMPLE DNA could not be created',
                                                            index, fullnumber, e)
                        logger.error(msg)
