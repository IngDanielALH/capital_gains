import sys
import json
import re
from capital_gains.configuration import ConfigLoader
from capital_gains.dto.TransactionDTO import TransactionDTO
from capital_gains.service import parse_operations


def main():
    config_loader = ConfigLoader()
    config = config_loader.config

    if config:
        tax_percentage = config.get('taxes', {}).get('sell', {}).get('percentage', 0.0)
        limit_without_tax = config.get('taxes', {}).get('sell', {}).get('limit_without_taxes', 0.0)

        input_data = sys.stdin.read().strip()

        input_data = re.sub(r']\s*\[', ']\n\n[', input_data)

        json_blocks = input_data.split("\n\n")

        results = []
        for block in json_blocks:
            try:
                operations = [
                    TransactionDTO.Builder()
                    .set_operation(t["operation"])
                    .set_unit_cost(t["unit-cost"])
                    .set_quantity(t["quantity"])
                    .build()
                    for t in json.loads(block)  # Procesamos cada JSON individualmente
                ]
                results.append(parse_operations(operations, tax_percentage, limit_without_tax))
            except json.JSONDecodeError:
                print("Error al parsear información de entrada")

        for result in results:
            print(json.dumps(result))


if __name__ == "__main__":
    main()
