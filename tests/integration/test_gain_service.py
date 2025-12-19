import json
import unittest

from capital_gains.dto.transaction_dto import TransactionDTO
from capital_gains.service.gains_service import parse_operations


class TestGainService(unittest.TestCase):
    def test_case_1(self):
        transactions_json = '''
        [{"operation": "buy", "unit-cost": 10.00, "quantity": 100},
        {"operation": "sell", "unit-cost": 15.00, "quantity": 50},
        {"operation": "sell", "unit-cost": 15.00, "quantity": 50}]
        '''

        operations = [
            TransactionDTO.Builder()
            .set_operation(t["operation"])
            .set_unit_cost(t["unit-cost"])
            .set_quantity(t["quantity"])
            .build()
            for t in json.loads(transactions_json)
        ]

        result = list(parse_operations(operations, 20, 20000))

        expected = [{"tax": 0.00}, {"tax": 0.00}, {"tax": 0.00}]

        self.assertEqual(expected, result)

    def test_case_2(self):
        transactions_json = '''
        [{"operation":"buy", "unit-cost":10.00, "quantity": 10000},
        {"operation":"sell", "unit-cost":20.00, "quantity": 5000},
        {"operation":"sell", "unit-cost":5.00, "quantity": 5000}]
        '''

        operations = [
            TransactionDTO.Builder()
            .set_operation(t["operation"])
            .set_unit_cost(t["unit-cost"])
            .set_quantity(t["quantity"])
            .build()
            for t in json.loads(transactions_json)
        ]

        result = list(parse_operations(operations, 20, 20000))

        expected = [{"tax": 0.00}, {"tax": 10000.00}, {"tax": 0.00}]

        self.assertEqual(expected, result)

    def test_case_3(self):
        transactions_json = '''
        [{"operation":"buy", "unit-cost":10.00, "quantity": 10000},
        {"operation":"sell", "unit-cost":5.00, "quantity": 5000},
        {"operation":"sell", "unit-cost":20.00, "quantity": 3000}]
        '''

        operations = [
            TransactionDTO.Builder()
            .set_operation(t["operation"])
            .set_unit_cost(t["unit-cost"])
            .set_quantity(t["quantity"])
            .build()
            for t in json.loads(transactions_json)
        ]

        result = list(parse_operations(operations, 20, 20000))

        expected = [{"tax": 0.00}, {"tax": 0.00}, {"tax": 1000.00}]

        self.assertEqual(expected, result)

    def test_case_4(self):
        transactions_json = '''
        [{"operation":"buy", "unit-cost":10.00, "quantity": 10000},
        {"operation":"buy", "unit-cost":25.00, "quantity": 5000},
        {"operation":"sell", "unit-cost":15.00, "quantity": 10000}]
        '''

        operations = [
            TransactionDTO.Builder()
            .set_operation(t["operation"])
            .set_unit_cost(t["unit-cost"])
            .set_quantity(t["quantity"])
            .build()
            for t in json.loads(transactions_json)
        ]

        result = list(parse_operations(operations, 20, 20000))

        expected = [{"tax": 0.00}, {"tax": 0.00}, {"tax": 0.00}]

        self.assertEqual(expected, result)

    def test_case_5(self):
        transactions_json = '''
        [{"operation":"buy", "unit-cost":10.00, "quantity": 10000},
        {"operation":"buy", "unit-cost":25.00, "quantity": 5000},
        {"operation":"sell", "unit-cost":15.00, "quantity": 10000},
        {"operation":"sell", "unit-cost":25.00, "quantity": 5000}]
        '''

        operations = [
            TransactionDTO.Builder()
            .set_operation(t["operation"])
            .set_unit_cost(t["unit-cost"])
            .set_quantity(t["quantity"])
            .build()
            for t in json.loads(transactions_json)
        ]

        result = list(parse_operations(operations, 20, 20000))

        expected = [{"tax": 0.00}, {"tax": 0.00}, {"tax": 0.00}, {"tax": 10000.00}]

        self.assertEqual(expected, result)

    def test_case_6(self):
        transactions_json = '''
        [{"operation":"buy", "unit-cost":10.00, "quantity": 10000},
        {"operation":"sell", "unit-cost":2.00, "quantity": 5000},
        {"operation":"sell", "unit-cost":20.00, "quantity": 2000},
        {"operation":"sell", "unit-cost":20.00, "quantity": 2000},
        {"operation":"sell", "unit-cost":25.00, "quantity": 1000}]
        '''

        operations = [
            TransactionDTO.Builder()
            .set_operation(t["operation"])
            .set_unit_cost(t["unit-cost"])
            .set_quantity(t["quantity"])
            .build()
            for t in json.loads(transactions_json)
        ]

        result = list(parse_operations(operations, 20, 20000))

        expected = [{"tax": 0.00}, {"tax": 0.00}, {"tax": 0.00}, {"tax": 0.00}, {"tax": 3000.00}]

        self.assertEqual(expected, result)

    def test_case_7(self):
        transactions_json = '''
        [{"operation":"buy", "unit-cost":10.00, "quantity": 10000},
        {"operation":"sell", "unit-cost":2.00, "quantity": 5000},
        {"operation":"sell", "unit-cost":20.00, "quantity": 2000},
        {"operation":"sell", "unit-cost":20.00, "quantity": 2000},
        {"operation":"sell", "unit-cost":25.00, "quantity": 1000},
        {"operation":"buy", "unit-cost":20.00, "quantity": 10000},
        {"operation":"sell", "unit-cost":15.00, "quantity": 5000},
        {"operation":"sell", "unit-cost":30.00, "quantity": 4350},
        {"operation":"sell", "unit-cost":30.00, "quantity": 650}]
        '''

        operations = [
            TransactionDTO.Builder()
            .set_operation(t["operation"])
            .set_unit_cost(t["unit-cost"])
            .set_quantity(t["quantity"])
            .build()
            for t in json.loads(transactions_json)
        ]

        result = list(parse_operations(operations, 20, 20000))

        expected = [{"tax": 0.00}, {"tax": 0.00}, {"tax": 0.00}, {"tax": 0.00}, {"tax": 3000.00},
                    {"tax": 0.00}, {"tax": 0.00}, {"tax": 3700.00}, {"tax": 0.00}]

        self.assertEqual(expected, result)

    def test_case_8(self):
        transactions_json = '''
        [{"operation":"buy", "unit-cost":10.00, "quantity": 10000},
        {"operation":"sell", "unit-cost":50.00, "quantity": 10000},
        {"operation":"buy", "unit-cost":20.00, "quantity": 10000},
        {"operation":"sell", "unit-cost":50.00, "quantity": 10000}]
        '''

        operations = [
            TransactionDTO.Builder()
            .set_operation(t["operation"])
            .set_unit_cost(t["unit-cost"])
            .set_quantity(t["quantity"])
            .build()
            for t in json.loads(transactions_json)
        ]

        result = list(parse_operations(operations, 20, 20000))

        expected = [{"tax": 0.00}, {"tax": 80000.00}, {"tax": 0.00}, {"tax": 60000.00}]

        self.assertEqual(expected, result)

    def test_case_9(self):
        transactions_json = '''
        [{"operation":"buy", "unit-cost": 5000.00, "quantity": 10},
        {"operation":"sell", "unit-cost": 4000.00, "quantity": 5},
        {"operation":"buy", "unit-cost": 15000.00, "quantity": 5},
        {"operation":"buy", "unit-cost": 4000.00, "quantity": 2},
        {"operation":"buy", "unit-cost": 23000.00, "quantity": 2},
        {"operation":"sell", "unit-cost": 20000.00, "quantity": 1},
        {"operation":"sell", "unit-cost": 12000.00, "quantity": 10},
        {"operation":"sell", "unit-cost": 15000.00, "quantity": 3}]
        '''

        operations = [
            TransactionDTO.Builder()
            .set_operation(t["operation"])
            .set_unit_cost(t["unit-cost"])
            .set_quantity(t["quantity"])
            .build()
            for t in json.loads(transactions_json)
        ]

        result = list(parse_operations(operations, 20, 20000))

        expected = [{"tax": 0}, {"tax": 0}, {"tax": 0}, {"tax": 0}, {"tax": 0}, {"tax": 0}, {"tax": 1000},
                    {"tax": 2400}]

        self.assertEqual(expected, result)

    def test_case_boundary_limit_exceeded(self):
        transactions_json = '''
        [{"operation": "buy", "unit-cost": 10.00, "quantity": 1000},
        {"operation": "sell", "unit-cost": 20.00001, "quantity": 1000}]
        '''

        operations = [
            TransactionDTO.Builder()
            .set_operation(t["operation"])
            .set_unit_cost(t["unit-cost"])
            .set_quantity(t["quantity"])
            .build()
            for t in json.loads(transactions_json)
        ]

        result = list(parse_operations(operations, 20, 20000))

        expected = [{"tax": 0.00}, {"tax": 2000.00}]

        self.assertEqual(expected, result)

    def test_case_accumulated_losses(self):
        transactions_json = '''
        [{"operation": "buy", "unit-cost": 100.00, "quantity": 100},
        {"operation": "sell", "unit-cost": 90.00, "quantity": 10},
        {"operation": "sell", "unit-cost": 90.00, "quantity": 10},
        {"operation": "sell", "unit-cost": 150.00, "quantity": 80}]
        '''

        operations = [
            TransactionDTO.Builder()
            .set_operation(t["operation"])
            .set_unit_cost(t["unit-cost"])
            .set_quantity(t["quantity"])
            .build()
            for t in json.loads(transactions_json)
        ]

        result = list(parse_operations(operations, 20, 20000))

        expected = [{"tax": 0.00}, {"tax": 0.00}, {"tax": 0.00}, {"tax": 0.00}]

        self.assertEqual(expected, result)

    def test_case_inventory_reset(self):
        transactions_json = '''
        [{"operation": "buy", "unit-cost": 10.00, "quantity": 1000},
        {"operation": "sell", "unit-cost": 10.00, "quantity": 1000},
        {"operation": "buy", "unit-cost": 50.00, "quantity": 1000},
        {"operation": "sell", "unit-cost": 80.00, "quantity": 1000}]
        '''

        operations = [
            TransactionDTO.Builder()
            .set_operation(t["operation"])
            .set_unit_cost(t["unit-cost"])
            .set_quantity(t["quantity"])
            .build()
            for t in json.loads(transactions_json)
        ]

        result = list(parse_operations(operations, 20, 20000))

        expected = [{"tax": 0.00}, {"tax": 0.00}, {"tax": 0.00}, {"tax": 6000.00}]

        self.assertEqual(expected, result)

    def test_case_wap_rounding(self):
        transactions_json = '''
        [{"operation": "buy", "unit-cost": 10.00, "quantity": 3000},
        {"operation": "buy", "unit-cost": 10.05, "quantity": 3000},
        {"operation": "sell", "unit-cost": 20.00, "quantity": 6000}]
        '''

        operations = [
            TransactionDTO.Builder()
            .set_operation(t["operation"])
            .set_unit_cost(t["unit-cost"])
            .set_quantity(t["quantity"])
            .build()
            for t in json.loads(transactions_json)
        ]

        result = list(parse_operations(operations, 20, 20000))

        expected = [{"tax": 0.00}, {"tax": 0.00}, {"tax": 11964.00}]

        self.assertEqual(expected, result)
