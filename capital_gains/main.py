import sys
import json

from capital_gains.configuration import ConfigLoader
from capital_gains.dto.TransactionDTO import TransactionDTO
from capital_gains.service import parse_operations


def main():
    print("Inicio del sistema")

    config_loader = ConfigLoader()
    config = config_loader.config

    if config:
        tax_percentage = config.get('taxes', {}).get('sell', {}).get('percentage', 0.0)
        limit_without_tax = config.get('taxes', {}).get('sell', {}).get('limit_without_taxes', 0.0)
        print(f"Impuesto sobre ganancias: {tax_percentage}%")
        print(f"Limite de ganancias antes de impuestos: ${limit_without_tax}")

        input_data = sys.stdin.read()

        try:
            operations = [
                TransactionDTO.Builder()
                .set_operation(t["operation"])
                .set_unit_cost(t["unit-cost"])
                .set_quantity(t["quantity"])
                .build()
                for t in json.loads(input_data)
            ]
            print(parse_operations(operations, tax_percentage, limit_without_tax))

        except json.JSONDecodeError:
            print("Error al parsear información de entrada")


if __name__ == '__main__':
    main()
