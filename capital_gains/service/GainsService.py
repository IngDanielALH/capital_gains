from decimal import Decimal, ROUND_HALF_UP
from capital_gains.dto.TaxDTO import TaxDTO
from capital_gains.utils.Constants import Constants

TWO_PLACES = Decimal("0.00")


def calculate_weighted_price(total_quantity, quantity, weighted_average_price, unit_cost):

    total_value = (total_quantity * weighted_average_price) + (quantity * unit_cost)
    new_total_quantity = total_quantity + quantity

    if new_total_quantity == 0:
        return Decimal("0.00")

    weighted_avg = total_value / new_total_quantity

    return weighted_avg.quantize(TWO_PLACES, rounding=ROUND_HALF_UP)


def parse_operations(operations, tax_percentage, limit_without_tax):

    weighted_average_price = Decimal("0.00")
    total_quantity = Decimal("0")
    total_lose = Decimal("0.00")

    tax_rate = Decimal(str(tax_percentage)) / Decimal("100")
    limit_tax = Decimal(str(limit_without_tax))

    is_first_buy = True
    result = []

    for operation in operations:
        current_operation = operation.get_operation()
        unit_cost = Decimal(str(operation.get_unit_cost()))
        quantity = Decimal(str(operation.get_quantity()))

        if current_operation == Constants.BUY_OPERATION:
            if is_first_buy:
                weighted_average_price = unit_cost
                total_quantity = quantity
                is_first_buy = False
            else:
                weighted_average_price = calculate_weighted_price(
                    total_quantity, quantity, weighted_average_price, unit_cost
                )
                total_quantity += quantity

            result.append(TaxDTO(0.0))
            continue

        sell_total_amount = unit_cost * quantity
        purchase_cost = weighted_average_price * quantity
        benefit = sell_total_amount - purchase_cost

        tax_amount = Decimal("0.00")

        if sell_total_amount > limit_tax:
            if total_lose < 0:
                new_benefit = benefit + total_lose
                if new_benefit >= 0:
                    raw_tax = new_benefit * tax_rate
                    tax_amount = raw_tax.quantize(TWO_PLACES, rounding=ROUND_HALF_UP)
                    total_lose = Decimal("0.00")
                else:
                    total_lose = new_benefit
                    tax_amount = Decimal("0.00")
            else:
                if benefit > 0:
                    raw_tax = benefit * tax_rate
                    tax_amount = raw_tax.quantize(TWO_PLACES, rounding=ROUND_HALF_UP)
                else:
                    tax_amount = Decimal("0.00")

                if benefit < 0:
                    total_lose += benefit

        else:
            if benefit < 0:
                total_lose += benefit

        result.append(TaxDTO(float(tax_amount)))
        total_quantity -= quantity

    return [tax.to_dict() for tax in result]