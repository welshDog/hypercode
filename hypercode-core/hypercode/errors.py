class HyperCodeError(Exception):
    """Base class for all HyperCode exceptions."""
    def __init__(self, message: str, line: int = 0, col: int = 0):
        self.message = message
        self.line = line
        self.col = col
        super().__init__(self.message)

    def __str__(self):
        return f"HyperCodeError(line {self.line}, col {self.col}): {self.message}"
