import unittest
from io import StringIO
from unittest.mock import patch, MagicMock
from capital_gains.main import main


class TestMainFunction(unittest.TestCase):

    @patch('sys.stdin', new_callable=StringIO)
    @patch('sys.stdout', new_callable=StringIO)
    @patch('capital_gains.main.ConfigLoader')
    def test_main_multiple_json_inputs(self, mock_config_loader, mock_stdout, mock_stdin):
        mock_config = {
            'taxes': {'sell': {'percentage': 20, 'limit_without_taxes': 20000}}
        }
        mock_instance = MagicMock()
        mock_instance.config = mock_config
        mock_config_loader.return_value = mock_instance

        mock_stdin.write('''[{"operation":"buy", "unit-cost":10.00, "quantity": 100},
{"operation":"sell", "unit-cost":15.00, "quantity": 50},
{"operation":"sell", "unit-cost":15.00, "quantity": 50}]

[{"operation":"buy", "unit-cost":10.00, "quantity": 10000},
{"operation":"sell", "unit-cost":20.00, "quantity": 5000},
{"operation":"sell", "unit-cost":5.00, "quantity": 5000}]''')
        mock_stdin.seek(0)

        # Ejecutar main()
        main()

        # Capturar salida
        output = mock_stdout.getvalue().strip()

        # Construir salida esperada
        expected_output = "[{'tax': 0}, {'tax': 0}, {'tax': 0}]\n[{'tax': 0}, {'tax': 10000.0}, {'tax': 0}]"

        self.assertEqual(output, expected_output)

    @patch('sys.stdin', new_callable=StringIO)
    @patch('sys.stdout', new_callable=StringIO)
    @patch('capital_gains.main.ConfigLoader')
    def test_main_multiple_json_inputs_no_space(self, mock_config_loader, mock_stdout, mock_stdin):
        mock_config = {
            'taxes': {'sell': {'percentage': 20, 'limit_without_taxes': 20000}}
        }
        mock_instance = MagicMock()
        mock_instance.config = mock_config
        mock_config_loader.return_value = mock_instance

        mock_stdin.write('''[{"operation":"buy", "unit-cost":10.00, "quantity": 100},
    {"operation":"sell", "unit-cost":15.00, "quantity": 50},
    {"operation":"sell", "unit-cost":15.00, "quantity": 50}]
    [{"operation":"buy", "unit-cost":10.00, "quantity": 10000},
    {"operation":"sell", "unit-cost":20.00, "quantity": 5000},
    {"operation":"sell", "unit-cost":5.00, "quantity": 5000}]''')
        mock_stdin.seek(0)

        # Ejecutar main()
        main()

        # Capturar salida
        output = mock_stdout.getvalue().strip()

        # Construir salida esperada
        expected_output = "[{'tax': 0}, {'tax': 0}, {'tax': 0}]\n[{'tax': 0}, {'tax': 10000.0}, {'tax': 0}]"

        self.assertEqual(output, expected_output)
