from server.test_utils import BaseTestCase

class RestaurantFormsTestCase(BaseTestCase):
    fixtures = [
        'test_fixtures/one_restaurant.json',
        'test_fixtures/user.json',
    ]

    def test_guest(self):
        """
        A guest can see any restaurant.
        A guest cannot edit any restaurant.
        A guest cannot create any restaurant.
        A guest cannot delete any restaurant.
        """
        response = self.client.get('/api/restaurant/1/')
        self.assertEqual(response.status_code, 200)

        response = self.post('/api/restaurant/', {})
        self.assertEqual(response.status_code, 403)

        response = self.post('/api/restaurant/1/', {'name': 'foo'})
        self.assertEqual(response.status_code, 403)

        response = self.client.delete('/api/restaurant/1/')
        self.assertEqual(response.status_code, 403)

    def test_user(self):
        """
        A user can see any restaurant.
        A user cannot edit any restaurant.
        A user cannot create any restaurant.
        A user cannot delete any restaurant.
        """
        self.login('user')

        response = self.client.get('/api/restaurant/1/')
        self.assertEqual(response.status_code, 200)

        response = self.post('/api/restaurant/', {})
        self.assertEqual(response.status_code, 403)

        response = self.post('/api/restaurant/1/', {})
        self.assertEqual(response.status_code, 403)

        response = self.client.delete('/api/restaurant/1/')
        self.assertEqual(response.status_code, 403)

    def test_owner_own(self):
        """
        A owner can see any restaurant.
        A owner can edit own restaurant.
        A owner can create own restaurant.
        A owner can delete own restaurant.
        """
        owner = self.create_user('owner2', role='owner')
        self.login(owner.username)

        response = self.client.get('/api/restaurant/1/')
        self.assertEqual(response.status_code, 200)

        restaurant_details = {'name': 'Food palace', 'description': 'The best'}
        response = self.post('/api/restaurant/', restaurant_details)
        self.assertEqual(response.status_code, 200)
        for key in restaurant_details:
            self.assertEqual(response.json()[key], restaurant_details[key])
        restaurant_id = response.json()['id']

        new_details = {'name': 'foo', 'description': 'bar' }
        response = self.post(f'/api/restaurant/{restaurant_id}/', new_details)
        self.assertEqual(response.status_code, 200)
        for key in new_details:
            self.assertEqual(response.json()[key], new_details[key])

        response = self.client.delete(f'/api/restaurant/{restaurant_id}/')
        self.assertEqual(response.status_code, 200)

    def test_owner_other(self):
        """
        A owner cannot edit other owner's restaurant.
        A owner cannot delete other owner's restaurant.
        """
        owner = self.create_user('owner2', role='owner')
        self.login(owner.username)

        response = self.client.get('/api/restaurant/1/')
        self.assertEqual(response.status_code, 200)

        response = self.post('/api/restaurant/1/', {})
        self.assertEqual(response.status_code, 403)

        response = self.client.delete('/api/restaurant/1/')
        self.assertEqual(response.status_code, 403)

