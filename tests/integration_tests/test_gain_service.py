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
        # Datos de las operaciones
        transactions_data = [
            (Constants.BUY_OPERATION, 10.00, 100),
            (Constants.SELL_OPERATION, 15.00, 50),
            (Constants.SELL_OPERATION, 15.00, 50)
        ]

        # Crear las operaciones con un bucle
        operations = [create_transaction(op, cost, qty) for op, cost, qty in transactions_data]
        result = parse_operations(operations, 20, 20000)
        expected = [{"tax": 0.00}, {"tax": 0.00}, {"tax": 0.00}]

        self.assertEqual(expected, result)
