import sys
import json

from capital_gains.configuration import ConfigLoader


def main():
    print("Inicio del sistema")

    config_loader = ConfigLoader()
    config = config_loader.config
    if config:
        tax_percentage = config.get('taxes', {}).get('sell', {}).get('percentage', 0.0)
        print(f"Impuesto sobre ganancias: {tax_percentage}%")

    input_data = sys.stdin.read()

    try:
        operations = json.loads(input_data)
        for operation in operations:
            print(f"Operación: {operation['operation']}, "
                  f"Precio unitario: {operation['unit-cost']}, "
                  f"Cantidad: {operation['quantity']}")
    except json.JSONDecodeError:
        print("Error al parsear información de entrada")


if __name__ == '__main__':
    main()
