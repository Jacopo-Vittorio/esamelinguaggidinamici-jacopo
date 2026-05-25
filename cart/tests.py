from django.test import TestCase


class CartRouteTest(TestCase):
    def test_checkout_buttons_route_to_order_create(self):
        response = self.client.get('/cart/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "window.location='/order/create/'", count=2)
