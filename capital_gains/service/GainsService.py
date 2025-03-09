from capital_gains.dto.TaxDTO import TaxDTO
from capital_gains.utils.Constants import Constants


def calculate_weighted_price(total_quantity, quantity, weighted_average_price, unit_cost):
    new_price = ((total_quantity * weighted_average_price) + (quantity * unit_cost)) / (total_quantity + quantity)
    return round(new_price, 2)


def parse_operations(operations, tax_percentage, limit_without_tax):
    weighted_average_price = 0
    total_quantity = 0
    is_first_buy = True
    result = []
    total_lose = 0

    for operation in operations:
        current_operation = operation.get_operation()
        unit_cost = operation.get_unit_cost()
        quantity = operation.get_quantity()
        pay_taxes = False

        if current_operation == Constants.BUY_OPERATION:

            if is_first_buy:
                weighted_average_price = unit_cost
                is_first_buy = False
                total_quantity = quantity
            else:
                weighted_average_price = calculate_weighted_price(
                    total_quantity, quantity, weighted_average_price, unit_cost
                )
                total_quantity += quantity

            result.append(TaxDTO(0))
            continue

        # Cálculo para ventas
        sell_total_amount = unit_cost * quantity
        purchase_cost = weighted_average_price * quantity
        benefit = sell_total_amount - purchase_cost

        if total_lose < 0 and not benefit < limit_without_tax:
            if abs(total_lose) >= benefit:
                total_lose += benefit
                benefit = 0
            else:
                benefit += total_lose
                total_lose = 0

        if benefit < 0:
            total_lose += benefit
            result.append(TaxDTO(0))
        else:
            if sell_total_amount > limit_without_tax:
                pay_taxes = True

            if pay_taxes and benefit > 0:
                tax_amount = round(benefit * (tax_percentage / 100), 2)
                result.append(TaxDTO(tax_amount))
            else:
                result.append(TaxDTO(0))

        total_quantity -= quantity

        if total_quantity == 0:
            weighted_average_price = 0

    return [tax.to_dict() for tax in result]
