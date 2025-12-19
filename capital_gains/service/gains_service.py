from decimal import Decimal
from capital_gains.service.portfolio_state import PortfolioState, STRATEGIES


def parse_operations(operations, tax_percentage, limit_without_tax):
    """
        Orchestrates the processing of financial operations to calculate capital gains taxes.

        This function acts as the main entry point for the business logic. It initializes
        the portfolio state and iterates through the input stream of operations.
        It utilizes the **Strategy Pattern** to delegate the specific logic (Buy/Sell)
        to the appropriate handler, ensuring adherence to the Open/Closed Principle.

        It implements **Lazy Loading** by yielding results one by one, allowing the
        application to process massive datasets with constant memory usage (O(1)).

        Args:
            operations (Iterator[TransactionDTO]): A stream of transaction objects to process.
            tax_percentage (float | int): The tax rate to apply on profits (e.g., 20).
            limit_without_tax (float | int): The monetary threshold for tax exemption (e.g., 20000).

        Yields:
            dict: A dictionary containing the calculated tax for the processed operation.
        """
    state = PortfolioState()

    tax_rate = Decimal(str(tax_percentage)) / Decimal("100")
    limit_tax = Decimal(str(limit_without_tax))
    tax_config = (tax_rate, limit_tax)

    for operation in operations:
        op_type = operation.get_operation()

        strategy = STRATEGIES.get(op_type)

        if not strategy:
            continue

        result_dto = strategy.execute(state, operation, tax_config)

        yield result_dto.to_dict()
