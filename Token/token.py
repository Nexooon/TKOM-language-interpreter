import typing
from Source.source_position import SourcePosition
from Token.token_type import TokenType


class Token:
    def __init__(self, type: TokenType, value: typing.Union[str, int, float], source_position: SourcePosition):
        self.type = type
        self.value = value
        self.position = source_position

    def __str__(self):
        return f"{self.position} type: {self.type} value: {self.value}"

    def __eq__(self, other: object):
        return self.type == other.type and self.value == other.value and self.position == other.position
