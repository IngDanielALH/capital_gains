import json
import unittest

from capital_gains.dto.TransactionDTO import TransactionDTO
from capital_gains.service.GainsService import parse_operations


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

        result = parse_operations(operations, 20, 20000)

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

        result = parse_operations(operations, 20, 20000)

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

        result = parse_operations(operations, 20, 20000)

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

        result = parse_operations(operations, 20, 20000)

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

        result = parse_operations(operations, 20, 20000)

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

        result = parse_operations(operations, 20, 20000)

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

        result = parse_operations(operations, 20, 20000)

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

        result = parse_operations(operations, 20, 20000)

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

        result = parse_operations(operations, 20, 20000)

        expected = [{"tax": 0}, {"tax": 0}, {"tax": 0}, {"tax": 0}, {"tax": 0}, {"tax": 0}, {"tax": 1000},
                    {"tax": 2400}]

        self.assertEqual(expected, result)

    def test_case_boundary_limit_exceeded(self):
        # Compra: 1000 * 10 = 10,000
        # Venta: 1000 * 20.00001 = 20,000.01 (Supera límite de 20k -> Paga impuestos)
        # Ganancia: 10,000.01 -> Tax 20%: 2,000.002 -> Redondeado: 2000.00
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

        result = parse_operations(operations, 20, 20000)

        expected = [{"tax": 0.00}, {"tax": 2000.00}]

        self.assertEqual(expected, result)

    def test_case_accumulated_losses(self):
        # 1. Buy 100 @ 100
        # 2. Sell 10 @ 90 -> Total 900 (<20k). Loss = -100.
        # 3. Sell 10 @ 90 -> Total 900 (<20k). Loss = -100. (Total Loss = -200)
        # 4. Sell 80 @ 150 -> Total 12,000 (<20k). Profit 4000. Tax = 0 (por monto < 20k).
        #    NOTA: Según reglas, ganancia exenta NO consume pérdidas acumuladas.
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

        result = parse_operations(operations, 20, 20000)

        expected = [{"tax": 0.00}, {"tax": 0.00}, {"tax": 0.00}, {"tax": 0.00}]

        self.assertEqual(expected, result)

    def test_case_inventory_reset(self):
        # 1. Buy @ 10. WAP = 10.
        # 2. Sell All. Qty = 0.
        # 3. Buy @ 50. New WAP debe ser 50 (no afectado por el 10 anterior).
        # 4. Sell @ 80. Profit = (80-50)*1000 = 30,000. Tax 20% = 6,000.
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

        result = parse_operations(operations, 20, 20000)

        expected = [{"tax": 0.00}, {"tax": 0.00}, {"tax": 0.00}, {"tax": 6000.00}]

        self.assertEqual(expected, result)

    def test_case_wap_rounding(self):
        # 1. Buy 3000 @ 10.
        # 2. Buy 3000 @ 10.05.
        #    WAP Exacto = 10.025.
        #    WAP Redondeado (Half Up) = 10.03.
        # 3. Sell 6000 @ 20.
        #    Costo con redondeo: 6000 * 10.03 = 60,180.
        #    Profit: 120,000 - 60,180 = 59,820.
        #    Tax 20%: 11,964.00.
        #    (Sin redondeo el tax sería 11,970.00)
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

        result = parse_operations(operations, 20, 20000)

        expected = [{"tax": 0.00}, {"tax": 0.00}, {"tax": 11964.00}]

        self.assertEqual(expected, result)