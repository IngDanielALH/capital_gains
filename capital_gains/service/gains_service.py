from decimal import Decimal

from capital_gains.dto.error import Error
from capital_gains.service.portfolio_state import PortfolioState, STRATEGIES
from capital_gains.utils.constants import Constants


def parse_operations(operations, tax_percentage, limit_without_tax):
    """
    Orchestrates the processing of financial operations to calculate capital gains taxes.

    It implements the logic to block the account after 3 consecutive validation errors.
    """
    state = PortfolioState()

    tax_rate = Decimal(str(tax_percentage)) / Decimal("100")
    limit_tax = Decimal(str(limit_without_tax))
    tax_config = (tax_rate, limit_tax)

    for operation in operations:

        # 1. REGLA DE BLOQUEO: Verificamos antes de intentar cualquier cosa.
        # Si la cuenta ya se bloqueó (en la iteración anterior o justo en la anterior),
        # rechazamos cualquier operación nueva.
        if state.is_blocked:
            yield Error(Constants.BLOCKED_ACCOUNT_ERROR).to_dict()
            continue

        op_type = operation.get_operation()
        strategy = STRATEGIES.get(op_type)

        if not strategy:
            continue

        try:
            # 2. INTENTO DE EJECUCIÓN
            result_dto = strategy.execute(state, operation, tax_config)

            # 3. ÉXITO
            # Si la ejecución fue correcta, reiniciamos el contador de errores consecutivos.
            state.reset_validation_errors()

            # Emitimos el resultado exitoso
            yield result_dto.to_dict()

        except ValueError:
            # 4. FALLO DE NEGOCIO (Stock insuficiente)

            # A) Registramos el error en el estado.
            # Si llegamos a 3, state.is_blocked se volverá True internamente.
            state.record_validation_error()

            # B) Emitimos SIEMPRE el error específico de la operación ("Can't sell...")
            yield Error(Constants.OUT_OF_STOCK_ERROR).to_dict()