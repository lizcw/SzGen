from django.test import TestCase


# Home page tests
class HomePageTests(TestCase):

    def test_home_page_status_code(self):
        response = self.client.get('/')
        self.assertEquals(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get('/')
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/index.html')

    def test_home_page_contains_correct_html(self):
        response = self.client.get('/')
        print(response)
        self.assertContains(response, 'Welcome to the SZGEN Database')

    def test_home_page_does_not_contain_incorrect_html(self):
        response = self.client.get('/')
        self.assertNotContains(
            response, 'Hi there! I should not be on the page.')





