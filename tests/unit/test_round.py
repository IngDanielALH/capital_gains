import unittest
from decimal import Decimal
from capital_gains.utils.math_utils import calculate_weighted_price


class TestRound(unittest.TestCase):

    def test_calculate_weighted_price(self):
        total_quantity = Decimal("5000")
        quantity = Decimal("10000")
        weighted_average_price = Decimal("10")
        unit_cost = Decimal("20")

        expected = Decimal("16.67")

        result = calculate_weighted_price(total_quantity, quantity, weighted_average_price, unit_cost)

        self.assertEqual(expected, result)
