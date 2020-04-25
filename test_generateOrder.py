import json
from unittest import TestCase

from customerClient import generateOrder


class TestGenerateOrder(TestCase):
    def test_generateOrder(self):
        order = generateOrder('2345')
        self.assertIsInstance(order, str)
        try:
            jsonOrder = json.loads(order)
        except ValueError:
            self.fail()
        self.assertIn('local_ip', jsonOrder)
        self.assertEqual(jsonOrder['local_ip'], '2345')
        self.assertGreaterEqual(len(jsonOrder.keys()), 2)
