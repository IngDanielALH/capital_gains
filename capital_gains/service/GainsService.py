from capital_gains.dto.TaxDTO import TaxDTO
from capital_gains.utils.Constants import Constants


def calculate_weighted_price(total_quantity, quantity, weighted_average_price, unit_cost):
    return round(((total_quantity * weighted_average_price) + (quantity * unit_cost)) / (total_quantity + quantity), 2)


def parse_operations(operations, tax_percentage, limit_without_tax):
    weighted_average_price = 0
    total_quantity = 0
    total_lose = 0
    is_first_buy = True
    result = []

    for operation in operations:
        current_operation, unit_cost, quantity = (
            operation.get_operation(),
            operation.get_unit_cost(),
            operation.get_quantity(),
        )

        if current_operation == Constants.BUY_OPERATION:
            if is_first_buy:
                weighted_average_price, total_quantity, is_first_buy = unit_cost, quantity, False
            else:
                weighted_average_price = calculate_weighted_price(total_quantity, quantity, weighted_average_price,
                                                                  unit_cost)
                total_quantity += quantity

            result.append(TaxDTO(0))
            continue

        sell_total_amount = unit_cost * quantity
        purchase_cost = weighted_average_price * quantity
        benefit = sell_total_amount - purchase_cost

        tax_amount = 0
        if sell_total_amount > limit_without_tax:
            if total_lose < 0:
                new_benefit = benefit + total_lose
                if new_benefit >= 0:
                    tax_amount = round(new_benefit * (tax_percentage / 100), 2)
                    total_lose = 0
                else:
                    total_lose = new_benefit
            else:
                tax_amount = round(benefit * (tax_percentage / 100), 2) if benefit > 0 else 0
                total_lose += benefit if benefit < 0 else 0

        else:
            total_lose += benefit if benefit < 0 else 0

        result.append(TaxDTO(tax_amount))
        total_quantity -= quantity

    return [tax.to_dict() for tax in result]
