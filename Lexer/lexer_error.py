from Source.source_position import SourcePosition


class LexerError(Exception):
    def __init__(self, message: str, position: SourcePosition):
        self.message = message
        self.position = position

    def __str__(self) -> str:
        return f"LexerError: {self.position} : {self.message}"
