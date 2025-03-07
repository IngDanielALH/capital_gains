import json
import unittest

from capital_gains.dto.TransactionDTO import TransactionDTO
from capital_gains.utils.Constants import Constants
from capital_gains.service.GainsService import parse_operations


def create_transaction(operation, unit_cost, quantity):
    return (TransactionDTO.Builder()
            .set_operation(operation)
            .set_unit_cost(unit_cost)
            .set_quantity(quantity)
            .build())


class TestGainService(unittest.TestCase):
    def test_case_1(self):

        transactions_json = '''
        [
            {"operation": "buy", "unit-cost": 10.00, "quantity": 100},
            {"operation": "sell", "unit-cost": 15.00, "quantity": 50},
            {"operation": "sell", "unit-cost": 15.00, "quantity": 50}
        ]
        '''

        operations = [
            TransactionDTO.Builder()
            .set_operation(t["operation"])
            .set_unit_cost(t["unit-cost"])
            .set_quantity(t["quantity"])
            .build()
            for t in json.loads(transactions_json)
        ]

        result = parse_operations(operations, 20, 20000)

        expected = [{"tax": 0.00}, {"tax": 0.00}, {"tax": 0.00}]

        self.assertEqual(expected, result)
