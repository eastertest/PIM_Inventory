import unittest
from django.test import Client


class SimpleTest(unittest.TestCase):
    def setUp(self):
        # Every test needs a client.
        self.client = Client()

    def test_details(self):
        # Issue a GET request.
        response = self.client.get('/admin/')

        # Check that the response is a 302 redirect to login
        self.assertEqual(response.status_code, 302)
