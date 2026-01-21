class Error:
    def __init__(self, error):
        self._error = error

    def get_error(self):
        return self._error

    def set_error(self, error):
        self._error = error

    def to_dict(self):
        return {"error": self._error}