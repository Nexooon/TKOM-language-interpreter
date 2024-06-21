class SourcePosition:
    def __init__(self, line: int, column: int):
        self.line = line
        self.column = column

    def __str__(self) -> str:
        return f"Ln {self.line} Col {self.column}"

    def __repr__(self) -> str:
        return f"Ln {self.line} Col {self.column}"

    def __eq__(self, other: object) -> bool:
        return self.line == other.line and self.column == other.column

    def advance(self):
        return SourcePosition(self.line, self.column + 1)

    def next_line(self):
        return SourcePosition(self.line + 1, 1)
