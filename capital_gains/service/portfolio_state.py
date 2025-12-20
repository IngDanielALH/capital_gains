from abc import ABC, abstractmethod
from decimal import Decimal, ROUND_HALF_UP
from capital_gains.dto.tax_dto import TaxDTO
from capital_gains.utils.constants import Constants
from capital_gains.utils.math_utils import calculate_weighted_price


TWO_PLACES = Decimal("0.00")


class PortfolioState:
    """
    Maintains the mutable state of the stock portfolio.

    This class acts as a context holder that persists across multiple operations,
    tracking the weighted average price, total inventory, and accumulated losses.

    Attributes:
        weighted_average_price (Decimal): The current weighted average price (WAP) of stocks.
        total_quantity (Decimal): The total number of stocks currently held.
        total_lose (Decimal): Accumulated financial losses from previous operations (stored as a negative value).
    """

    def __init__(self):
        self.weighted_average_price = Decimal("0.00")
        self.total_quantity = Decimal("0")
        self.total_lose = Decimal("0.00")


class OperationStrategy(ABC):
    """
    Abstract base class defining the contract for financial operation strategies.

    Follows the Strategy Pattern to enforce a common interface for processing
    different types of transactions (e.g., Buy, Sell).
    """

    @abstractmethod
    def execute(self, state: PortfolioState, operation, tax_config) -> TaxDTO:
        """
        Executes the business logic for a specific operation and updates the portfolio state.

        Args:
            state (PortfolioState): The current mutable state of the portfolio.
            operation (TransactionDTO): The transaction data (unit cost, quantity).
            tax_config (tuple): A tuple containing (tax_rate, tax_exemption_limit).

        Returns:
            TaxDTO: A data transfer object containing the calculated tax amount.
        """
        pass


class BuyStrategy(OperationStrategy):
    """
    Implements the logic for a 'Buy' operation.

    This strategy assumes that buying stocks never generates a tax event.
    Its primary responsibility is to recalculate the Weighted Average Price (WAP)
    and update the total quantity in the portfolio state.
    """
    def execute(self, state: PortfolioState, operation, tax_config) -> TaxDTO:
        """
                Executes the logic for a 'Buy' operation.

                This method is responsible for updating the portfolio's Weighted Average Price (WAP)
                and increasing the total quantity of stocks held.

                Note:
                    Buying stocks does not trigger a tax event, so this method always returns 0.0 tax.
                    The `tax_config` parameter is present to satisfy the `OperationStrategy` interface
                    but is ignored in this implementation.

                Args:
                    state (PortfolioState): The current mutable state of the portfolio to update.
                    operation (TransactionDTO): The purchase transaction details (unit cost, quantity).
                    tax_config (tuple): Tax configuration (unused in this strategy).

                Returns:
                    TaxDTO: A DTO containing 0.0 as the tax amount.
                """
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
    """
    Implements the logic for a 'Sell' operation.

    This strategy handles profit calculation, loss deduction, and tax application.
    """
    def execute(self, state: PortfolioState, operation, tax_config) -> TaxDTO:
        """
        Executes a sell operation applying the specific tax rules.

        Business Rules:
        1. **Loss Generation:** If the sale results in a loss, no tax is paid, and the
           loss is accumulated in `state.total_lose` to offset future gains.
        2. **Tax Exemption:** If the total sell amount is below the limit (e.g., 20,000),
           no tax is paid, even if there is a profit.
        3. **Loss Deduction:** If there is a taxable profit, accumulated losses from
           previous operations are deducted before calculating the tax.

        Args:
            state (PortfolioState): The current portfolio state (updated in place).
            operation (TransactionDTO): The sell transaction details.
            tax_config (tuple): Configuration containing (tax_rate, limit_tax).

        Returns:
            TaxDTO: The calculated tax amount (0.00 if exempt or loss).
        """
        unit_cost = Decimal(str(operation.get_unit_cost()))
        quantity = Decimal(str(operation.get_quantity()))

        if state.total_quantity < quantity:
            raise ValueError(
                f"Insufficient stock. Owned: {state.total_quantity}, Selling: {quantity}"
            )

        tax_rate, limit_tax = tax_config

        sell_total_amount = unit_cost * quantity
        purchase_cost = state.weighted_average_price * quantity
        benefit = sell_total_amount - purchase_cost

        state.total_quantity -= quantity

        if benefit < 0:
            state.total_lose += benefit
            return TaxDTO(0.0)

        if sell_total_amount <= limit_tax:
            return TaxDTO(0.0)

        taxable_amount = benefit + state.total_lose

        if taxable_amount > 0:
            state.total_lose = Decimal("0.00")
            raw_tax = taxable_amount * tax_rate
            tax_amount = raw_tax.quantize(TWO_PLACES, rounding=ROUND_HALF_UP)
            return TaxDTO(float(tax_amount))

        else:
            state.total_lose = taxable_amount
            return TaxDTO(0.0)


STRATEGIES = {
    Constants.BUY_OPERATION: BuyStrategy(),
    Constants.SELL_OPERATION: SellStrategy()
}