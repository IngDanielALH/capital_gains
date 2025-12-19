from decimal import Decimal
from capital_gains.service.portfolio_state import PortfolioState, STRATEGIES


def parse_operations(operations, tax_percentage, limit_without_tax):

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
