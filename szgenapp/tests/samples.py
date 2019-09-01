from django.http import HttpRequest
from django.test import TestCase, SimpleTestCase
from django.urls import reverse
import datetime

from szgenapp.models.studies import Study, STATUS_CHOICES
from szgenapp.models.participants import Participant, PARTICIPANT_STATUS_CHOICES, StudyParticipant, COUNTRY_CHOICES
from szgenapp.models.samples import *


class SamplesPageTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Set up data for the whole TestCase
        # Maybe locations should be generated?
        cls.loc1 = Location.objects.create(tank=1, shelf=3, cell=5)
        cls.loc2 = Location.objects.create(tank=2, shelf=3, cell=5)
        cls.loc3 = Location.objects.create(tank=3, shelf=3, cell=5)
        # Create a Study
        cls.study = Study.objects.create(title="TestStudy", precursor="T", description="My test study",
                                         status=STATUS_CHOICES[0])
        # Create a participant (no study)
        cls.participant = Participant.objects.create(alphacode="ABC",
                                                     country=COUNTRY_CHOICES[0],
                                                     secondaryid="ABC001",
                                                     status=PARTICIPANT_STATUS_CHOICES[0],
                                                     npid=1460001,
                                                     )
        # Add a participant to a study with IDs
        cls.studyparticipant = StudyParticipant.objects.create(participant=cls.participant,
                                                               study=cls.study,
                                                               fullnumber='',
                                                               family='123',
                                                               individual='001')
        # Create a Sample for this studyparticipant
        cls.sample = Sample.objects.create(participant=cls.studyparticipant,
                                           sample_type=SAMPLE_TYPES[0],
                                           rebleed=False,
                                           arrival_date=datetime.date(2009, 9, 5),
                                           notes='Test sample')
        # Process sample to subsamples with own locations, indicate subsample number
        cls.lc001 = SubSample.objects.create(sample=cls.sample,
                                             sample_type=SAMPLE_TYPES[0],
                                             sample_num=1,
                                             used=True,
                                             storage_date=datetime.date(2010, 10, 6),
                                             used_date=datetime.date(2010, 12, 6),
                                             notes='Leukocyte sample',
                                             location=cls.loc1)

        cls.lc2 = SubSample.objects.create(sample=cls.sample,
                                           sample_type=SAMPLE_TYPES[0],
                                           sample_num=2,
                                           used=False,
                                           storage_date=datetime.date(2010, 10, 6),
                                           used_date=None,
                                           notes='Leukocyte sample',
                                           location=cls.loc2)
        cls.lcl = SubSample.objects.create(sample=cls.sample,
                                           sample_type=SAMPLE_TYPES[1],
                                           sample_num=1,
                                           used=True,
                                           storage_date=datetime.date(2010, 10, 6),
                                           used_date=None,
                                           notes='LCL sample',
                                           location=cls.loc3)
        cls.ship = Shipment.objects.create(sample=cls.sample,
                                           shipment_date=datetime.date(2012, 12, 12),
                                           reference='A1234',
                                           notes='Test Shipment',
                                           rutgers_number='Z123456')

    def test_page_status_code(self):
        response = self.client.get('/samples/')
        self.assertEquals(response.status_code, 200)

    def test_view_url_by_name(self):
        response = self.client.get(reverse('samples'))
        self.assertEquals(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('samples'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'sample/sample-list.html')

    def test_page_contains_correct_html(self):
        response = self.client.get('/samples/')
        self.assertContains(response, 'Samples</h2>')

    def test_page_does_not_contain_incorrect_html(self):
        response = self.client.get('/samples/')
        self.assertNotContains(
            response, 'Welcome to the SZGEN Database')

    def test_sample_subsample(self):
        self.assertEqual(self.sample.subsample_set.count(), 3)

    def test_sample_qc(self):
        qc1 = QC.objects.create(subsample=self.lc001, qc_date=datetime.date(2013, 1, 2), passed=False)
        qc2 = QC.objects.create(subsample=self.lc001, qc_date=datetime.date(2013, 1, 3), passed=True)
        qc3 = QC.objects.create(subsample=self.lcl, qc_date=datetime.date(2013, 1, 4), passed=True)
        self.assertEqual(self.lc001.sample_qc.count(), 2)
        self.assertEqual(self.lcl.sample_qc.count(), 1)
        self.assertEqual(self.lc001.get_qc_result(), qc2)
        self.assertEqual(self.lc001.sample_qc.order_by('-qc_date').first(), qc2)

    def test_sample_shipment(self):
        self.assertEqual(self.sample.shipment_set.first().id, 1)
        self.assertEqual(self.sample.shipment_set.first().rutgers_number, self.ship.rutgers_number)

    def test_sample_transform(self):
        tfm = TransformSample.objects.create(sample=self.sample, transform_date=datetime.date(2010, 12, 2),
                                             failed=False, notes='Test Transform')
        self.assertEqual(self.sample.transformsample_set.count(), 1)

    def test_sample_harvest(self):
        tfm = HarvestSample.objects.create(sample=self.sample,
                                           regrow_date=datetime.date(2010, 12, 5),
                                           harvest_date=datetime.date(2010, 12, 9),
                                           complete=False,
                                           notes='Test Harvest')
        self.assertEqual(self.sample.harvestsample_set.count(), 1)
