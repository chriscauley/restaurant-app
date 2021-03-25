from django.test import Client

from server.test_utils import BaseTestCase

class ViewsTestCase(BaseTestCase):
    fixtures = ['test_fixtures/user.json']

    def test_usersettings_form(self):
        response = self.client.get('/api/settings/?schema=1')
        self.assertEqual(
            list(response.json()['schema']['properties'].keys()),
            ['username', 'avatar_url']
        )

        # Cannot get any user settings unless loged in
        response = self.client.get('/api/settings/2/')
        self.assertEqual(response.status_code, 403)

        # user can get own data
        self.login('user')
        response = self.client.get('/api/settings/self/')
        self.assertEqual(response.json()['id'], 2)
        response = self.client.get('/api/settings/2/')
        self.assertEqual(response.json()['id'], 2)

        # user cannot see other people's data
        response = self.client.get('/api/settings/1/')
        self.assertEqual(response.status_code, 403)

        # user cannot update other pepole's data
        response = self.post('/api/settings/1/', {'username': 'new_username'})
        self.assertEqual(response.status_code, 403)

        # user can update own data
        response = self.post('/api/settings/self/', {'username': 'new_username'})
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/api/settings/2/')
        self.assertEqual(response.json()['username'], 'new_username')
