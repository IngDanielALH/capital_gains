from capital_gains.utils.Constants import Constants


def calculate_weighted_price(total_quantity, quantity, weighted_average_price, unit_cost):
    new_price = ((total_quantity * weighted_average_price) + (quantity * unit_cost)) / (total_quantity + quantity)
    return round(new_price, 2)


def parse_operations(operations, tax_percentage, limit_without_tax):
    weighted_average_price = operations[0]["unit-cost"]
    is_first_buy = True
    tax = 0
    total_quantity = 0

    for operation in operations:
        current_operation = operation["operation"]
        unit_cost = operation["unit-cost"]
        quantity = operation["quantity"]

        if Constants.BUY_OPERATION == current_operation:
            if is_first_buy:
                weighted_average_price = unit_cost
                is_first_buy = False
                total_quantity = quantity
            else:
                weighted_average_price = calculate_weighted_price(total_quantity, quantity, weighted_average_price,
                                                                  unit_cost)
        else:
            purchase_cost = weighted_average_price * unit_cost
            sell_total_amount = unit_cost * quantity
            benefit = sell_total_amount - purchase_cost
            total_quantity -= quantity
            if benefit <= limit_without_tax:
                tax += 0
            else:
                tax += benefit - (benefit * tax_percentage / 100)
        print(f"Tax for operation {current_operation} of {quantity} at price of {unit_cost} is {tax}")

    pass
