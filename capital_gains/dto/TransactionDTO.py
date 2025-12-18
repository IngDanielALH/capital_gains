class TransactionDTO:
    __slots__ = ['_operation', '_unit_cost', '_quantity']

    def __init__(self, operation: str, unit_cost: float, quantity: int):
        self._operation = operation
        self._unit_cost = unit_cost
        self._quantity = quantity

    # Getters
    def get_operation(self) -> str:
        return self._operation

    def get_unit_cost(self) -> float:
        return self._unit_cost

    def get_quantity(self) -> int:
        return self._quantity

    def __repr__(self):
        return f"TransactionDTO(operation={self._operation}, unit_cost={self._unit_cost}, quantity={self._quantity})"

    class Builder:
        def __init__(self):
            self._operation = None
            self._unit_cost = None
            self._quantity = None

        def set_operation(self, operation: str):
            self._operation = operation
            return self

        def set_unit_cost(self, unit_cost: float):
            self._unit_cost = unit_cost
            return self

        def set_quantity(self, quantity: int):
            self._quantity = quantity
            return self

        def build(self):
            return TransactionDTO(self._operation, self._unit_cost, self._quantity)