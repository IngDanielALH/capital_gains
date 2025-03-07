from capital_gains.dto.TaxDTO import TaxDTO
from capital_gains.utils.Constants import Constants


def calculate_weighted_price(total_quantity, quantity, weighted_average_price, unit_cost):
    new_price = ((total_quantity * weighted_average_price) + (quantity * unit_cost)) / (total_quantity + quantity)
    return round(new_price, 2)


def parse_operations(operations, tax_percentage, limit_without_tax):
    # Acceder al unit-cost del primer objeto correctamente usando el getter
    weighted_average_price = operations[0].get_unit_cost()
    is_first_buy = True
    total_quantity = 0
    result = []
    benefit = 0

    for operation in operations:
        # Usar los métodos getters en lugar de índices
        current_operation = operation.get_operation()
        unit_cost = operation.get_unit_cost()
        quantity = operation.get_quantity()

        if Constants.BUY_OPERATION == current_operation:
            if is_first_buy:
                weighted_average_price = unit_cost
                is_first_buy = False
                total_quantity = quantity
            else:
                weighted_average_price = calculate_weighted_price(
                    total_quantity, quantity, weighted_average_price, unit_cost
                )
        else:
            purchase_cost = weighted_average_price * quantity
            sell_total_amount = unit_cost * quantity
            benefit = sell_total_amount - purchase_cost
            total_quantity -= quantity

        if benefit <= limit_without_tax or current_operation == Constants.BUY_OPERATION:
            result.append(TaxDTO(0))
        else:
            result.append(TaxDTO(benefit * (tax_percentage / 100)))

    return [tax.to_dict() for tax in result]


