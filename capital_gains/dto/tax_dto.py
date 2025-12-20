class TaxDTO:

    def __init__(self, tax: float):
        self._tax = tax

    def get_tax(self) -> float:
        return self._tax

    def set_tax(self, tax: float):
        self._tax = tax

    def to_dict(self):
        return {"tax": float(self._tax)}

    def __repr__(self):
        return f"TaxDTO(tax={self._tax})"
