import json
import unittest

# Ajusta los imports según tu estructura de carpetas real
from capital_gains.dto.transaction_dto import TransactionDTO
from capital_gains.service.gains_service import parse_operations


def _parse_input(json_str):
    """Helper para evitar repetir el Builder en cada test"""
    return [
        TransactionDTO.Builder()
        .set_operation(t["operation"])
        .set_unit_cost(t["unit-cost"])
        .set_quantity(t["quantity"])
        .set_fee(t.get("fee", 0))  # Manejo seguro de opcionales
        .build()
        for t in json.loads(json_str)
    ]


class TestBrokerFees(unittest.TestCase):

    def test_fee_increases_wap_on_buy(self):
        """
        Caso 1: El fee en la compra se suma al costo, subiendo el WAP.
        Compra: 10000 * 10 + 500 fee = 100,500 total.
        WAP = 10.05
        Venta: 10000 * 20 = 200,000.
        Ganancia: 200,000 - 100,500 = 99,500.
        Impuesto (20%): 19,900.
        """
        transactions_json = '''
        [
            {"operation": "buy", "unit-cost": 10.00, "quantity": 10000, "fee": 500.00},
            {"operation": "sell", "unit-cost": 20.00, "quantity": 10000}
        ]
        '''

        operations = _parse_input(transactions_json)
        result = list(parse_operations(operations, 20, 20000))
        expected = [{"tax": 0.00}, {"tax": 19900.00}]

        self.assertEqual(expected, result)

    def test_fee_reduces_profit_on_sell(self):
        """
        Caso 2: El fee en la venta reduce la ganancia gravable.
        Compra: 10000 * 10 = 100,000. WAP = 10.
        Venta: 10000 * 20 = 200,000. Fee = 500.
        Ganancia Bruta: 100,000.
        Ganancia Neta: 100,000 - 500 = 99,500.
        Impuesto (20%): 19,900.
        """
        transactions_json = '''
        [
            {"operation": "buy", "unit-cost": 10.00, "quantity": 10000},
            {"operation": "sell", "unit-cost": 20.00, "quantity": 10000, "fee": 500.00}
        ]
        '''

        operations = _parse_input(transactions_json)
        result = list(parse_operations(operations, 20, 20000))
        expected = [{"tax": 0.00}, {"tax": 19900.00}]

        self.assertEqual(expected, result)

    def test_fee_can_turn_profit_into_loss(self):
        """
        Caso 3: Venta 'break-even' (mismo precio) con fee genera pérdida.
        Compra: 10000 a 10.
        Venta: 10000 a 10. Fee 100.
        Ganancia: 0 - 100 = -100 (Pérdida).
        Impuesto: 0.
        """
        transactions_json = '''
        [
            {"operation": "buy", "unit-cost": 10.00, "quantity": 10000},
            {"operation": "sell", "unit-cost": 10.00, "quantity": 10000, "fee": 100.00}
        ]
        '''

        operations = _parse_input(transactions_json)
        result = list(parse_operations(operations, 20, 20000))
        expected = [{"tax": 0.00}, {"tax": 0.00}]

        self.assertEqual(expected, result)