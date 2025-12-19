from decimal import Decimal, ROUND_HALF_UP
from capital_gains.service.PortfolioState import PortfolioState, STRATEGIES


def parse_operations(operations, tax_percentage, limit_without_tax):
    # 1. Inicializar Estado
    state = PortfolioState()

    # 2. Preparar Configuración
    tax_rate = Decimal(str(tax_percentage)) / Decimal("100")
    limit_tax = Decimal(str(limit_without_tax))
    tax_config = (tax_rate, limit_tax)

    # 3. Iterar usando Polimorfismo
    for operation in operations:
        op_type = operation.get_operation()

        # Obtenemos la estrategia correspondiente (Buy o Sell)
        strategy = STRATEGIES.get(op_type)

        if not strategy:
            # Manejo de error si llega una operación desconocida
            # Podrías yieldear un error, ignorar, o lanzar excepción
            continue

            # Delegamos la lógica a la estrategia
        result_dto = strategy.execute(state, operation, tax_config)

        yield result_dto.to_dict()
