import json
import unittest

from capital_gains.dto.transaction_dto import TransactionDTO
from capital_gains.service.gains_service import parse_operations
from capital_gains.utils.constants import Constants


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

    def test_case_inventory_validation_error(self):
        transactions_json = '''
        [{"operation": "buy", "unit-cost": 10.00, "quantity": 100},
        {"operation": "sell", "unit-cost": 20.00, "quantity": 150}]
        '''

        operations = [
            TransactionDTO(t["operation"], t["unit-cost"], t["quantity"])
            for t in json.loads(transactions_json)
        ]

        expected = [{"tax": 0.00}, {"error": Constants.OUT_OF_STOCK_ERROR}]

        """with self.assertRaises(ValueError) as context:
            list(parse_operations(operations, 20, 20000))"""
        #self.assertIn("Insufficient stock", str(context.exception))

        result = list(parse_operations(operations, 20, 20000))
        self.assertEqual(expected, result)

    def test_case_inventory_validation_multiple_sells(self):
        transactions_json = '''
        [{"operation":"buy", "unit-cost": 10, "quantity": 10000}, {"operation":"sell", 
        "unit-cost":20, "quantity": 11000}, {"operation":"sell", "unit-cost": 10, "quantity": 5000}]
        '''

        operations = [
            TransactionDTO(t["operation"], t["unit-cost"], t["quantity"])
            for t in json.loads(transactions_json)
        ]

        expected = [{'tax': 0.0}, {'error': "Can't sell more stocks than you have"}, {'tax': 0.0}]

        result = list(parse_operations(operations, 20, 20000))
        self.assertEqual(expected, result)

    def test_case_independent_simulations(self):
        """
        Case #1 + Case #2:
        """

        json_line_1 = '''
        [{"operation":"buy", "unit-cost":10.00, "quantity": 100},
         {"operation":"sell", "unit-cost":15.00, "quantity": 50},
         {"operation":"sell", "unit-cost":15.00, "quantity": 50}]
        '''

        json_line_2 = '''
        [{"operation":"buy", "unit-cost":10.00, "quantity": 10000},
         {"operation":"sell", "unit-cost":20.00, "quantity": 5000},
         {"operation":"sell", "unit-cost":5.00, "quantity": 5000}]
        '''

        operations_1 = [
            TransactionDTO(t["operation"], t["unit-cost"], t["quantity"])
            for t in json.loads(json_line_1)
        ]
        result_1 = list(parse_operations(operations_1, 20, 20000))
        expected_1 = [{"tax": 0.0}, {"tax": 0.0}, {"tax": 0.0}]

        operations_2 = [
            TransactionDTO(t["operation"], t["unit-cost"], t["quantity"])
            for t in json.loads(json_line_2)
        ]
        result_2 = list(parse_operations(operations_2, 20, 20000))

        expected_2 = [{"tax": 0.0}, {"tax": 10000.0}, {"tax": 0.0}]

        self.assertEqual(expected_1, result_1)
        self.assertEqual(expected_2, result_2)

    def test_case_blocked_account(self):
        transactions_json = '''
        [{"operation":"sell", "unit-cost":20, "quantity": 10000},
{"operation":"sell", "unit-cost":20, "quantity": 10000},
{"operation":"sell", "unit-cost":20, "quantity": 10000},
{"operation":"buy", "unit-cost":10, "quantity": 10000}]
        '''

        operations = [
            TransactionDTO(t["operation"], t["unit-cost"], t["quantity"])
            for t in json.loads(transactions_json)
        ]

        expected = [{"error": "Can't sell more stocks than you have"},
                    {"error": "Can't sell more stocks than you have"},
                    {"error": "Can't sell more stocks than you have"},
                    {"error": "Your account is blocked"}]

        result = list(parse_operations(operations, 20, 20000))
        self.assertEqual(expected, result)

    def test_case_blocked_account_2(self):
            transactions_json = '''
            [{"operation":"sell", "unit-cost":20, "quantity": 10000},
    {"operation":"sell", "unit-cost":20, "quantity": 10000},
    {"operation":"sell", "unit-cost":20, "quantity": 10000},
    {"operation":"sell", "unit-cost":20, "quantity": 10000}]
            '''

            operations = [
                TransactionDTO(t["operation"], t["unit-cost"], t["quantity"])
                for t in json.loads(transactions_json)
            ]

            expected = [{"error": "Can't sell more stocks than you have"},
                        {"error": "Can't sell more stocks than you have"},
                        {"error": "Can't sell more stocks than you have"},
                        {"error": "Your account is blocked"}]

            result = list(parse_operations(operations, 20, 20000))
            self.assertEqual(expected, result)

    # --- Req 1: Stock Quantity Validation ---

    def test_sell_exactly_owned_quantity_succeeds(self):
        """Selling exactly the available quantity is valid (boundary case)."""
        operations = [
            TransactionDTO("buy", 10.00, 100),
            TransactionDTO("sell", 20.00, 100),
        ]
        result = list(parse_operations(operations, 20, 20000))
        expected = [{"tax": 0.0}, {"tax": 0.0}]
        self.assertEqual(expected, result)

    def test_sell_with_no_inventory_errors(self):
        """Selling when no stocks have been bought produces an error."""
        operations = [
            TransactionDTO("sell", 20.00, 1),
        ]
        result = list(parse_operations(operations, 20, 20000))
        expected = [{"error": "Can't sell more stocks than you have"}]
        self.assertEqual(expected, result)

    def test_failed_sell_preserves_inventory(self):
        """A failed oversell does not deduct from the existing inventory."""
        operations = [
            TransactionDTO("buy", 10.00, 100),
            TransactionDTO("sell", 20.00, 150),  # fails: only 100 available
            TransactionDTO("sell", 20.00, 100),  # succeeds: inventory was not reduced
        ]
        result = list(parse_operations(operations, 20, 20000))
        expected = [{"tax": 0.0}, {"error": "Can't sell more stocks than you have"}, {"tax": 0.0}]
        self.assertEqual(expected, result)

    # --- Req 2: Stock Quantity Error Limit (account blocking) ---

    def test_two_consecutive_errors_do_not_block(self):
        """Two consecutive errors followed by a success must NOT block the account."""
        operations = [
            TransactionDTO("sell", 20.00, 100),  # err #1
            TransactionDTO("sell", 20.00, 100),  # err #2
            TransactionDTO("buy", 10.00, 100),   # success → resets counter
            TransactionDTO("buy", 10.00, 100),   # must not be blocked
        ]
        result = list(parse_operations(operations, 20, 20000))
        expected = [
            {"error": "Can't sell more stocks than you have"},
            {"error": "Can't sell more stocks than you have"},
            {"tax": 0.0},
            {"tax": 0.0},
        ]
        self.assertEqual(expected, result)

    def test_success_resets_error_counter(self):
        """A successful operation resets the consecutive-error counter,
        so two separate groups of 2 errors never trigger a block."""
        operations = [
            TransactionDTO("sell", 20.00, 100),  # err #1 (consecutive=1)
            TransactionDTO("sell", 20.00, 100),  # err #2 (consecutive=2)
            TransactionDTO("buy", 10.00, 100),   # success → resets to 0
            TransactionDTO("sell", 20.00, 200),  # err #1 again (only 100 owned; consecutive=1)
            TransactionDTO("sell", 20.00, 200),  # err #2 again (consecutive=2)
            TransactionDTO("buy", 10.00, 100),   # success → resets to 0 again
        ]
        result = list(parse_operations(operations, 20, 20000))
        expected = [
            {"error": "Can't sell more stocks than you have"},
            {"error": "Can't sell more stocks than you have"},
            {"tax": 0.0},
            {"error": "Can't sell more stocks than you have"},
            {"error": "Can't sell more stocks than you have"},
            {"tax": 0.0},
        ]
        self.assertEqual(expected, result)

    def test_blocked_account_rejects_all_subsequent_operations(self):
        """Once blocked, every subsequent operation (buy or sell) is rejected."""
        operations = [
            TransactionDTO("sell", 20.00, 10000),  # err #1
            TransactionDTO("sell", 20.00, 10000),  # err #2
            TransactionDTO("sell", 20.00, 10000),  # err #3 → triggers block
            TransactionDTO("buy", 10.00, 10000),   # blocked
            TransactionDTO("buy", 10.00, 5000),    # blocked
            TransactionDTO("sell", 20.00, 1),      # blocked
        ]
        result = list(parse_operations(operations, 20, 20000))
        expected = [
            {"error": "Can't sell more stocks than you have"},
            {"error": "Can't sell more stocks than you have"},
            {"error": "Can't sell more stocks than you have"},
            {"error": "Your account is blocked"},
            {"error": "Your account is blocked"},
            {"error": "Your account is blocked"},
        ]
        self.assertEqual(expected, result)
