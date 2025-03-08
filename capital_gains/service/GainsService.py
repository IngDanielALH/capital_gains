from capital_gains.dto.TaxDTO import TaxDTO
from capital_gains.utils.Constants import Constants


def calculate_weighted_price(total_quantity, quantity, weighted_average_price, unit_cost):
    new_price = ((total_quantity * weighted_average_price) + (quantity * unit_cost)) / (total_quantity + quantity)
    return round(new_price, 2)


def parse_operations(operations, tax_percentage, limit_without_tax):
    weighted_average_price = operations[0].get_unit_cost()
    is_first_buy = True
    total_quantity = 0
    result = []
    total_lose = 0  # Pérdidas acumuladas

    for operation in operations:
        current_operation = operation.get_operation()
        unit_cost = operation.get_unit_cost()
        quantity = operation.get_quantity()
        pay_taxes = False

        if current_operation == Constants.BUY_OPERATION:
            if is_first_buy:
                weighted_average_price = unit_cost
                is_first_buy = False
                total_quantity = quantity
            else:
                weighted_average_price = calculate_weighted_price(
                    total_quantity, quantity, weighted_average_price, unit_cost
                )
            result.append(TaxDTO(0))  # No se paga impuestos en compras
            continue

        # Cálculo para ventas
        purchase_cost = weighted_average_price * quantity
        sell_total_amount = unit_cost * quantity
        benefit = sell_total_amount - purchase_cost

        # Aplicar deducción de pérdidas previas si existen
        if total_lose < 0:
            if abs(total_lose) >= benefit:
                total_lose += benefit  # Se usa toda la ganancia para reducir la pérdida
                benefit = 0  # No queda ganancia sujeta a impuestos
            else:
                benefit += total_lose  # Se compensa solo parte de la pérdida
                total_lose = 0  # Se ha compensado totalmente la pérdida previa

        if benefit < 0:
            # Si aún hay pérdida, la acumulamos y no pagamos impuestos
            total_lose += benefit
            result.append(TaxDTO(0))
        else:
            # Verificar si la venta total supera el límite de exención
            if sell_total_amount > limit_without_tax:
                pay_taxes = True

            if pay_taxes and benefit > 0:
                tax_amount = benefit * (tax_percentage / 100)
                result.append(TaxDTO(tax_amount))
            else:
                result.append(TaxDTO(0))

        # Actualizar la cantidad de acciones en posesión
        total_quantity -= quantity

    return [tax.to_dict() for tax in result]
