from django.test import TestCase, RequestFactory
from django.http import Http404
from points.views import fetch_options

class FetchOptionsViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_fetch_options_for_treasure_hunt(self):
        request = self.factory.get('/fetch-options/', {'type': 'treasure_hunt'}, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        response = fetch_options(request)
        self.assertEqual(response.status_code, 200)

    def test_fetch_options_for_quiz(self):
        request = self.factory.get('/fetch-options/', {'type': 'quiz'}, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        response = fetch_options(request)
        self.assertEqual(response.status_code, 200)

    def test_invalid_request(self):
        request = self.factory.get('/fetch-options/')
        with self.assertRaises(Http404):
            fetch_options(request)
