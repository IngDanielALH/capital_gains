import unittest
from capital_gains.service.GainsService import *


class TestGainsService(unittest.TestCase):
    def test_calculate_weighted_price(self):
        total_quantity = 5000
        quantity = 10000
        weighted_average_price = 10
        unit_cost = 20

        expected = 16.67
        result = calculate_weighted_price(total_quantity, quantity, weighted_average_price, unit_cost)

        self.assertEqual(expected, result)
