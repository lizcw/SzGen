from django.test import TestCase, Client
from django.urls import reverse


class DatasetsPageTests(TestCase):
    def setUp(self):
        self.client = Client(enforce_csrf_checks=True)

    def test_home_page_status_code(self):
        response = self.client.get('/datasets/')
        self.assertEquals(response.status_code, 200)

    def test_view_url_by_name(self):
        response = self.client.get(reverse('datasets'))
        self.assertEquals(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('datasets'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'dataset/dataset-list.html')

    def test_home_page_contains_correct_html(self):
        response = self.client.get('/datasets/')
        self.assertContains(response, 'Datasets')

    def test_home_page_does_not_contain_incorrect_html(self):
        response = self.client.get('/datasets/')
        self.assertNotContains(response, 'Welcome to the SZGEN Database')


