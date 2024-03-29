from django.test import TestCase
from django.urls import reverse

from szgenapp.models.participants import PARTICIPANT_STATUS_CHOICES, StudyParticipant, COUNTRY_CHOICES
from szgenapp.models.studies import Study, STATUS_CHOICES


class ParticipantsPageTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Set up data for the whole TestCase
        cls.study = Study.objects.create(title="TestStudy", precursor="T", description="My test study",
                                         status=STATUS_CHOICES[0])
        cls.studyparticipant = StudyParticipant.objects.create(participant=cls.participant,
                                                               study=cls.study,
                                                               fullnumber='',
                                                               family='123',
                                                               individual='001',
                                                               alphacode="ABC",
                                                               country=COUNTRY_CHOICES[0],
                                                               secondaryid="ABC001",
                                                               status=PARTICIPANT_STATUS_CHOICES[0],
                                                               npid=1460001, )

    def test_page_status_code(self):
        response = self.client.get('/participants/')
        self.assertEquals(response.status_code, 200)

    def test_view_url_by_name(self):
        response = self.client.get(reverse('participants'))
        self.assertEquals(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('participants'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'participant/participant-list.html')

    def test_page_contains_correct_html(self):
        response = self.client.get('/participants/')
        self.assertContains(response, '<h2>Participants</h2>')
        self.assertContains(response, 'href="/participant/create/"')

    def test_page_does_not_contain_incorrect_html(self):
        response = self.client.get('/participants/')
        self.assertNotContains(
            response, 'Welcome to the SZGEN Database')

    ### CREATE PARTICIPANT PAGES
    # UI TESTING /participant/create/
    # 1. Valid data - save
    # 1. Invalid data - error
    def test_create_page_status_code(self):
        response = self.client.get('/participant/create/')
        self.assertEquals(response.status_code, 200)

    def test_create_page_reverse(self):
        response = self.client.get(reverse('participant_create'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'participant/participant-create.html')

    def test_create_page_contains_correct_html(self):
        response = self.client.get('/participant/create/')
        self.assertContains(response, '<h3>Create Participant</h3>')

    ### TEST PARTICIPANT DATA
    def test_participant_id(self):
        self.assertEqual(self.studyparticipant.id, 1)

    def test_participant_fullnumber(self):
        self.assertEqual(self.studyparticipant.fullnumber, '')
        self.assertEqual(self.studyparticipant.getFullNumber(), 'T123-001')

    def test_participant_country(self):
        self.assertEqual(self.studyparticipant.country, ('INDIA', 'India'))
        self.assertEqual(self.studyparticipant.get_country_display(), "('INDIA', 'India')")

    def test_participant_alphacode(self):
        self.assertEqual(self.studyparticipant.alphacode, 'ABC')

    def test_participant_secondaryid(self):
        self.assertEqual(self.studyparticipant.secondaryid, 'ABC001')

    def test_participant_npid(self):
        self.assertEqual(self.studyparticipant.npid, 1460001)

    def test_participant_status(self):
        self.assertEqual(self.studyparticipant.status, ('ACTIVE', 'Active'))
        self.assertEqual(self.studyparticipant.get_status_display(), "('ACTIVE', 'Active')")

    def test_participant_study(self):
        self.assertEqual(self.studyparticipant.study, self.study)

    def test_participant_district(self):
        self.assertEqual(self.studyparticipant.district, '')

    def test_participant_family(self):
        self.assertEqual(self.studyparticipant.family, '123')

    def test_participant_individual(self):
        self.assertEqual(self.studyparticipant.individual, '001')

