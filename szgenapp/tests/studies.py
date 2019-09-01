from django.http import HttpRequest
from django.test import TestCase, SimpleTestCase
from django.urls import reverse
import datetime

from szgenapp.models.studies import Study, STATUS_CHOICES
from szgenapp.models.participants import Participant, PARTICIPANT_STATUS_CHOICES, StudyParticipant, COUNTRY_CHOICES
from szgenapp.models.samples import *

class StudyDetailsTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Set up data for the whole TestCase
        cls.study = Study.objects.create(title="TestStudy", precursor="T", description="My test study",
                                         status=STATUS_CHOICES[0])

    def test_details_page_status_code(self):
        response = self.client.get('/study/1/')
        self.assertEquals(response.status_code, 200)

    def test_view_url_by_name(self):
        response = self.client.get(reverse('study_detail', args=[1]))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'study/study.html')

    def test_view_uses_correct_template(self):
        response = self.client.get('/study/1/')
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'study/study.html')

    def test_page_contains_correct_html(self):
        response = self.client.get('/study/1/')
        self.assertContains(response, '<h3>Study TestStudy</h3>', 1)
        self.assertContains(response, 'href="/study/update/1/"')

    ### UPDATE STUDY PAGES
    # UI TESTING /study/update/1/
    # 1. Valid data - save
    # 1. Invalid data - error
    def test_update_page_status_code(self):
        response = self.client.get('/study/update/1/')
        self.assertEquals(response.status_code, 200)

    def test_update_page_reverse(self):
        response = self.client.get(reverse('study_update', args=[1]))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'study/study-create.html')

    ##TODO
    # def test_update_page_contains_correct_html(self):
    #     response = self.client.post('/study/update/1/', {'title': ''})
    #     self.assertFormError(response, 'title', 'errors', 'This field is required')
    ##

    ### CREATE STUDY PAGES
    # UI TESTING /study/create/
    # 1. Valid data - save
    # 1. Invalid data - error
    def test_create_page_status_code(self):
        response = self.client.get('/study/create/')
        self.assertEquals(response.status_code, 200)

    def test_create_page_reverse(self):
        response = self.client.get(reverse('study_create'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'study/study-create.html')

