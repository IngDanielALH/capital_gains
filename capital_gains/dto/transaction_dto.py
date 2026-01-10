class TransactionDTO:
    __slots__ = ['_operation', '_unit_cost', '_quantity', '_fee']

    def __init__(self, operation: str, unit_cost: float, quantity: int, fee: float = 0):
        self._operation = operation
        self._unit_cost = unit_cost
        self._quantity = quantity
        self._fee = fee

    # Getters
    def get_operation(self) -> str:
        return self._operation

    def get_unit_cost(self) -> float:
        return self._unit_cost

    def get_quantity(self) -> int:
        return self._quantity

    def get_fee(self) -> float:
        return self._fee

    def __repr__(self):
        return (f"TransactionDTO(operation={self._operation}, unit_cost={self._unit_cost}, quantity={self._quantity}, "
                f"fee={self._fee})")

    class Builder:
        def __init__(self):
            self._operation = None
            self._unit_cost = None
            self._quantity = None
            self._fee = None

        def set_operation(self, operation: str):
            self._operation = operation
            return self

        def set_unit_cost(self, unit_cost: float):
            self._unit_cost = unit_cost
            return self

        def set_quantity(self, quantity: int):
            self._quantity = quantity
            return self

        def set_fee(self, fee: float):
            self._fee = fee
            return self

        def build(self):
            return TransactionDTO(self._operation, self._unit_cost, self._quantity, self._fee)