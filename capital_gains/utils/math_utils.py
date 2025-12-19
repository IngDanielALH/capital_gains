# capital_gains/utils/math_utils.py
from decimal import Decimal, ROUND_HALF_UP

TWO_PLACES = Decimal("0.00")


def calculate_weighted_price(total_quantity, quantity, weighted_average_price, unit_cost):
    total_value = (total_quantity * weighted_average_price) + (quantity * unit_cost)
    new_total_quantity = total_quantity + quantity

    if new_total_quantity == 0:
        return Decimal("0.00")

    weighted_avg = total_value / new_total_quantity
    return weighted_avg.quantize(TWO_PLACES, rounding=ROUND_HALF_UP)
