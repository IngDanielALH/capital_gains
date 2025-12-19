from abc import ABC, abstractmethod
from decimal import Decimal, ROUND_HALF_UP
from capital_gains.dto.tax_dto import TaxDTO
from capital_gains.utils.constants import Constants
from capital_gains.utils.math_utils import calculate_weighted_price

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

        # Actualizamos la cantidad de acciones (esto pasa en cualquier venta)
        state.total_quantity -= quantity

        # CASO 1: Venta con pérdida
        # Si perdemos dinero, acumulamos la pérdida y no pagamos impuestos.
        # Esto aplica sin importar si el monto total supera o no el límite de 20k.
        if benefit < 0:
            state.total_lose += benefit
            return TaxDTO(0.0)

        # CASO 2: Venta exenta de impuestos (menor al límite)
        # Si llegamos aquí, el beneficio es >= 0.
        if sell_total_amount <= limit_tax:
            return TaxDTO(0.0)

        # CASO 3: Venta con ganancia y sujeta a impuestos (> límite)
        # Calculamos la ganancia neta restando las pérdidas acumuladas (state.total_lose es negativo)
        taxable_amount = benefit + state.total_lose

        # Si después de restar pérdidas seguimos teniendo ganancia:
        if taxable_amount > 0:
            state.total_lose = Decimal("0.00")  # Hemos "pagado" todas las pérdidas viejas
            raw_tax = taxable_amount * tax_rate
            tax_amount = raw_tax.quantize(TWO_PLACES, rounding=ROUND_HALF_UP)
            return TaxDTO(float(tax_amount))

        # Si la ganancia no alcanzó para cubrir todas las pérdidas viejas:
        else:
            state.total_lose = taxable_amount  # Actualizamos el saldo de pérdidas restante
            return TaxDTO(0.0)


# Mapa de estrategias (Factory simple)
STRATEGIES = {
    Constants.BUY_OPERATION: BuyStrategy(),
    Constants.SELL_OPERATION: SellStrategy()
}