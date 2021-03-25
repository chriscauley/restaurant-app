from server.test_utils import BaseTestCase
from server.restaurant.models import Order, OwnerBlock
from server.user.models import User

class OrderFlowTestCase(BaseTestCase):
    fixtures = [
        'test_fixtures/user.json',
        'test_fixtures/one_restaurant.json',
    ]

    def setUp(self):
        self.customer = User.objects.get(username='user')
        self.order = Order.objects.create(
            status='placed',
            restaurant_id=1,
            user_id=self.customer.id
        )

    def check_set_status(self, status, expected_code):
        response = self.post(f'/api/order/{self.order.id}/', {'status': status})
        self.assertEqual(response.status_code, expected_code)

    def test_guest_order_flow(self):
        """
        A guest sees no orders and cannot modify an order.
        """
        response = self.client.get('/api/orders/')
        self.assertEqual(len(response.json()['items']), 0)

        response = self.client.get(f'/api/order/{self.order.id}/')
        self.assertEqual(response.status_code, 404)

        self.check_set_status('placed', 404)
        self.check_set_status('canceled', 404)
        self.check_set_status('processing', 404)
        self.check_set_status('in_route', 404)
        self.check_set_status('delivered', 404)
        self.check_set_status('received', 404)


    def test_user_order_flow(self):
        """
        A user can place an order.
        A user can cancel a placed order.
        A user cannot un-cancel an order.
        A user can mark an delivered order as received.
        """

        self.login(self.customer.username)
        response = self.client.get('/api/orders/')
        self.assertEqual(len(response.json()['items']), 1)

        response = self.client.get(f'/api/order/{self.order.id}/')
        self.assertEqual(response.status_code, 200)

        # user can cancel order
        self.check_set_status('canceled', 200)

        # user cannot uncancel an order or set any other statuses
        self.check_set_status('placed', 403)
        self.check_set_status('canceled', 403)
        self.check_set_status('processing', 403)
        self.check_set_status('in_route', 403)
        self.check_set_status('delivered', 403)
        self.check_set_status('received', 403)

        # once delivered a user can again update the status
        self.order.status = 'delivered'
        self.order.save()
        self.check_set_status('received', 200)

    def test_owner_order_flow(self):
        """
        An owner cannot cancel a placed order.
        An owner can move an order from placed to delivered.
        An owner cannot mark an order as received.
        """

        self.login('owner')
        response = self.client.get('/api/orders/')
        self.assertEqual(len(response.json()['items']), 1)

        response = self.client.get(f'/api/order/{self.order.id}/')
        self.assertEqual(response.status_code, 200)

        # owner cannot cancel
        self.check_set_status('canceled', 403)

        # owner can move it from placed to delivered
        self.check_set_status('processing', 200)
        self.check_set_status('in_route', 200)
        self.check_set_status('delivered', 200)

        # owner cannot marke order as received
        self.check_set_status('received', 403)

    def test_owner_can_block_user(self):
        self.login('owner')
        response = self.post(f'/api/order/{self.order.id}/', {'action': 'block'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(OwnerBlock.objects.all()), 1)

        response = self.post(f'/api/order/{self.order.id}/', {'action': 'unblock'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(OwnerBlock.objects.all()), 0)

    def test_guest_cannot_block_user(self):
        response = self.post(f'/api/order/{self.order.id}/', {'action': 'block'})
        self.assertEqual(response.status_code, 404)

        response = self.post(f'/api/order/{self.order.id}/', {'action': 'unblock'})
        self.assertEqual(response.status_code, 404)

    def test_user_cannot_block_user(self):
        self.login('user')
        response = self.post(f'/api/order/{self.order.id}/', {'action': 'block'})
        self.assertEqual(response.status_code, 403)

        response = self.post(f'/api/order/{self.order.id}/', {'action': 'unblock'})
        self.assertEqual(response.status_code, 403)
