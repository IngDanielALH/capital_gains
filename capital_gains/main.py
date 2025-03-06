import sys
import json


def main():
    print("Inicio del sistema")
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
