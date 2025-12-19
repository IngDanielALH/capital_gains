# capital_gains/utils/math_utils.py
from decimal import Decimal, ROUND_HALF_UP

TWO_PLACES = Decimal("0.00")


def calculate_weighted_price(total_quantity, quantity, weighted_average_price, unit_cost):
    """
        Calculates the new Weighted Average Price (WAP) after a purchase.

        It weights the total value of the current holdings plus the value of the
        newly purchased stocks, divided by the new total quantity.

        Formula:
            WAP = ((Current_Qty * Current_WAP) + (New_Qty * New_Cost)) / (New_Total_Qty)

        Args:
            total_quantity (Decimal): The total number of stocks held before this transaction.
            quantity (Decimal): The number of new stocks acquired in this transaction.
            weighted_average_price (Decimal): The current weighted average price.
            unit_cost (Decimal): The unit cost of the new stocks.

        Returns:
            Decimal: The new weighted average price, rounded to 2 decimal places
            using the ROUND_HALF_UP strategy. Returns 0.00 if the new total quantity is 0.
        """
    total_value = (total_quantity * weighted_average_price) + (quantity * unit_cost)
    new_total_quantity = total_quantity + quantity

    if new_total_quantity == 0:
        return Decimal("0.00")

    weighted_avg = total_value / new_total_quantity
    return weighted_avg.quantize(TWO_PLACES, rounding=ROUND_HALF_UP)
