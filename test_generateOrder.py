import json
from unittest import TestCase

from customerMenu import CustomerClass


class TestGenerateOrder(TestCase):
    def test_generateOrder(self):
        screen = CustomerClass()
        order = screen.generateOrder('2345')
        self.assertIsInstance(order, str)
        try:
            jsonOrder = json.loads(order)
        except ValueError:
            self.fail()
        self.assertIn('local_ip', jsonOrder)
        self.assertEqual(jsonOrder['local_ip'], '2345')
