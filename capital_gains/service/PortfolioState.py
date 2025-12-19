from abc import ABC, abstractmethod
from decimal import Decimal, ROUND_HALF_UP
from capital_gains.dto.TaxDTO import TaxDTO
from capital_gains.utils.Constants import Constants
from capital_gains.utils.MathUtils import calculate_weighted_price

# Asumimos que esta función existe en tu contexto
# from ... import calculate_weighted_price

TWO_PLACES = Decimal("0.00")


class PortfolioState:
    """Encapsula el estado mutable de la cartera."""

    def __init__(self):
        self.weighted_average_price = Decimal("0.00")
        self.total_quantity = Decimal("0")
        self.total_lose = Decimal("0.00")


class OperationStrategy(ABC):
    """Interfaz abstracta para cualquier operación financiera."""

    @abstractmethod
    def execute(self, state: PortfolioState, operation, tax_config) -> TaxDTO:
        pass


class BuyStrategy(OperationStrategy):
    def execute(self, state: PortfolioState, operation, tax_config) -> TaxDTO:
        unit_cost = Decimal(str(operation.get_unit_cost()))
        quantity = Decimal(str(operation.get_quantity()))

        if state.total_quantity == 0:
            state.weighted_average_price = unit_cost
            state.total_quantity = quantity
        else:

            state.weighted_average_price = calculate_weighted_price(
                state.total_quantity, quantity, state.weighted_average_price, unit_cost
            )
            state.total_quantity += quantity

        return TaxDTO(0.0)


class SellStrategy(OperationStrategy):
    def execute(self, state: PortfolioState, operation, tax_config) -> TaxDTO:
        unit_cost = Decimal(str(operation.get_unit_cost()))
        quantity = Decimal(str(operation.get_quantity()))

        tax_rate, limit_tax = tax_config

        sell_total_amount = unit_cost * quantity
        purchase_cost = state.weighted_average_price * quantity
        benefit = sell_total_amount - purchase_cost

        tax_amount = Decimal("0.00")

        if sell_total_amount > limit_tax:
            if state.total_lose < 0:
                new_benefit = benefit + state.total_lose
                if new_benefit >= 0:
                    raw_tax = new_benefit * tax_rate
                    tax_amount = raw_tax.quantize(TWO_PLACES, rounding=ROUND_HALF_UP)
                    state.total_lose = Decimal("0.00")
                else:
                    state.total_lose = new_benefit
                    tax_amount = Decimal("0.00")
            else:
                if benefit > 0:
                    raw_tax = benefit * tax_rate
                    tax_amount = raw_tax.quantize(TWO_PLACES, rounding=ROUND_HALF_UP)
                else:
                    pass

                if benefit < 0:
                    state.total_lose += benefit
        else:
            if benefit < 0:
                state.total_lose += benefit

        state.total_quantity -= quantity
        return TaxDTO(float(tax_amount))


# Mapa de estrategias (Factory simple)
STRATEGIES = {
    Constants.BUY_OPERATION: BuyStrategy(),
    Constants.SELL_OPERATION: SellStrategy()
}