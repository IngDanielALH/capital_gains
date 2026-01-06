import sys
import json
from capital_gains.configuration.config_loader import ConfigLoader
from capital_gains.dto.transaction_dto import TransactionDTO
from capital_gains.service.gains_service import parse_operations


def main():
    config_loader = ConfigLoader()
    config = config_loader.config

    if config:
        tax_percentage = config.get('taxes', {}).get('sell', {}).get('percentage', 0.0)
        limit_without_tax = config.get('taxes', {}).get('sell', {}).get('limit_without_taxes', 0.0)

        if sys.stdin.isatty():
            print("Program ready. Please enter operations (JSON Array):", file=sys.stderr)

        for line in sys.stdin:
            line = line.strip()

            if not line:
                continue

            try:
                operations_data = json.loads(line)
                operations_generator = (
                    TransactionDTO.Builder()
                    .set_operation(t["operation"])
                    .set_unit_cost(t["unit-cost"])
                    .set_quantity(t["quantity"])
                    .build()
                    for t in operations_data
                )

                result_generator = parse_operations(operations_generator, tax_percentage, limit_without_tax)

                print(json.dumps(list(result_generator)))

            except json.JSONDecodeError:
                print(f"Error: Invalid JSON format provided -> {line}", file=sys.stderr)


if __name__ == "__main__":
    main()