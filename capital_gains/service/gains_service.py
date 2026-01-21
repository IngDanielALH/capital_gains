from decimal import Decimal

from capital_gains.dto.error import Error
from capital_gains.service.portfolio_state import PortfolioState, STRATEGIES
from capital_gains.utils.constants import Constants


def parse_operations(operations, tax_percentage, limit_without_tax):
    """
    Orchestrates the processing of financial operations...
    (Docstring original...)
    """
    state = PortfolioState()

    tax_rate = Decimal(str(tax_percentage)) / Decimal("100")
    limit_tax = Decimal(str(limit_without_tax))
    tax_config = (tax_rate, limit_tax)

    for operation in operations:

        # 1. REGLA DE BLOQUEO: Verificamos antes de intentar cualquier cosa.
        # Si la cuenta ya se bloqueó en la iteración anterior, cortamos aquí.
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

            # 3. ÉXITO: Si la línea anterior no falló, reiniciamos el contador
            # porque el requerimiento especifica errores "consecutivos".
            state.reset_validation_errors()

        except ValueError:
            # 4. FALLO: Manejamos la excepción de negocio (Stock insuficiente)

            # A) Registramos el error en el estado (aquí cuenta 1, 2, 3...)
            state.record_validation_error()

            # B) Generamos el error actual
            # Nota: Aunque sea el 3er error y state.is_blocked ya sea True internamente,
            # el requerimiento pide mostrar el error de "Can't sell" en esta línea,
            # y el "Blocked" hasta la siguiente.
            result_dto = Error(Constants.OUT_OF_STOCK_ERROR)

        yield result_dto.to_dict()
