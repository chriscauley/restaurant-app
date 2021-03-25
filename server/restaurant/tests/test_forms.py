from server.test_utils import BaseTestCase
from server.restaurant.models import MenuItem, Restaurant, MenuSection

class RestaurantFormsTestCase(BaseTestCase):
    fixtures = [
        'test_fixtures/user.json',
        'test_fixtures/one_restaurant.json',
    ]

    def _test_user_or_guest(self):
        response = self.client.get('/api/restaurant/1/')
        self.assertEqual(response.status_code, 200)

        response = self.post('/api/restaurant/', {})
        self.assertEqual(response.status_code, 403)

        response = self.post('/api/restaurant/1/', {})
        self.assertEqual(response.status_code, 403)

        response = self.client.delete('/api/restaurant/1/')
        self.assertEqual(response.status_code, 403)

    def test_guest(self):
        """
        A guest can see any restaurant.
        A guest cannot edit any restaurant.
        A guest cannot create any restaurant.
        A guest cannot delete any restaurant.
        """
        self._test_user_or_guest()

    def test_user(self):
        """
        A user can see any restaurant.
        A user cannot edit any restaurant.
        A user cannot create any restaurant.
        A user cannot delete any restaurant.
        """
        self.login('user')
        self._test_user_or_guest()

    def test_owner_own_restaurant(self):
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

    def test_owner_other_other_restaurant(self):
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

class MenuItemTestCase(BaseTestCase):
    fixtures = [
        'test_fixtures/one_restaurant.json',
        'test_fixtures/user.json',
    ]

    def _test_user_or_guest(self, do_create=True):
        response = self.client.get('/api/menuitem/1/')
        self.assertEqual(response.status_code, 200)

        if do_create:
            response = self.post('/api/menuitem/', {})
            self.assertEqual(response.status_code, 403)

        response = self.post('/api/menuitem/1/', {})
        self.assertEqual(response.status_code, 403)

        response = self.client.delete('/api/menuitem/1/')
        self.assertEqual(response.status_code, 403)

    def test_user(self):
        """
        An user is just like a guest with regards to CRUDing menuitems.
        """
        self.login('user')

        self._test_user_or_guest()

    def test_guest(self):
        self._test_user_or_guest()

    def test_owner_others_menuitem(self):
        """
        An owner is just like a guest with regards to other people's data
        """
        owner = self.create_user('owner2', role='owner')
        self.login(owner.username)

        self._test_user_or_guest(do_create=False)

    def test_owner_own_menuitem(self):
        """
        A owner can see any menuitem.
        A owner can edit own menuitem.
        A owner can create own menuitem.
        A owner can delete own menuitem.
        """
        self.login('owner') # This user owns everything in one_restaurant.json fixture
        restaurant = Restaurant.objects.filter(owner__username='owner').first()
        menusection = restaurant.menusection_set.all().first()

        response = self.client.get(f'/api/menuitem/1/')
        self.assertEqual(response.status_code, 200)

        menuitem_details = { 'name': 'Food', 'description': 'fuud', 'price': '1', 'menusection': menusection.id }
        response = self.post('/api/menuitem/', menuitem_details)
        self.assertEqual(response.status_code, 200)
        for key in menuitem_details:
            if key == 'menusection':
                continue # not returned with get_json
            self.assertEqual(response.json()[key], menuitem_details[key])
        menuitem_id = response.json()['id']

        new_details = { 'name': 'name2', 'description': 'description2', 'price': '2', 'menusection': menusection.id }
        response = self.post(f'/api/menuitem/{menuitem_id}/', new_details)
        self.assertEqual(response.status_code, 200)
        for key in new_details:
            if key == 'menusection':
                continue # not returned with get_json
            self.assertEqual(response.json()[key], new_details[key])

        response = self.client.delete(f'/api/menuitem/{menuitem_id}/')
        self.assertEqual(response.status_code, 200)

class MenusectionTestCase(BaseTestCase):
    fixtures = [
        'test_fixtures/one_restaurant.json',
        'test_fixtures/user.json',
    ]

    def _test_user_or_guest(self, do_create=True):
        response = self.client.get('/api/menusection/1/')
        self.assertEqual(response.status_code, 200)

        if do_create:
            response = self.post('/api/menusection/', {})
            self.assertEqual(response.status_code, 403)

        response = self.post('/api/menusection/1/', {})
        self.assertEqual(response.status_code, 403)

        response = self.client.delete('/api/menusection/1/')
        self.assertEqual(response.status_code, 403)

    def test_user(self):
        """
        An user is just like a guest with regards to CRUDing menusections.
        """
        self.login('user')

        self._test_user_or_guest()

    def test_guest(self):
        self._test_user_or_guest()

    def test_owner_others_menusection(self):
        """
        An owner is just like a guest with regards to other people's data
        """
        owner = self.create_user('owner2', role='owner')
        self.login(owner.username)

        self._test_user_or_guest(do_create=False)

    def test_owner_own_menusection(self):
        """
        A owner can see any menusection.
        A owner can edit own menusection.
        A owner can create own menusection.
        A owner can delete own menusection.
        """
        self.login('owner') # This user owns everything in one_restaurant.json fixture
        restaurant = Restaurant.objects.filter(owner__username='owner').first()

        response = self.client.get(f'/api/menusection/1/')
        self.assertEqual(response.status_code, 200)

        menusection_details = { 'name': 'Lunch', 'restaurant': restaurant.id }
        response = self.post('/api/menusection/', menusection_details)
        self.assertEqual(response.status_code, 200)
        for key in menusection_details:
            if key == 'restaurant':
                continue # not returned with get_json
            self.assertEqual(response.json()[key], menusection_details[key])
        menusection_id = response.json()['id']

        new_details = { 'name': 'dinner', 'restaurant': restaurant.id }
        response = self.post(f'/api/menusection/{menusection_id}/', new_details)
        self.assertEqual(response.status_code, 200)
        for key in new_details:
            if key == 'restaurant':
                continue # not returned with get_json
            self.assertEqual(response.json()[key], new_details[key])

        response = self.client.delete(f'/api/menusection/{menusection_id}/')
        self.assertEqual(response.status_code, 200)
