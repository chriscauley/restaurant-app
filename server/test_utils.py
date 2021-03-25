from django.test import TestCase, Client

PASSWORD = '1viPIjbvpYcvIt'

class BaseTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def post(self, url, data):
        return self.client.post(url, data, content_type='application/json')

    def login(self, username):
        data = {'username': username, 'password': PASSWORD}
        return self.post('/api/login/', data)
