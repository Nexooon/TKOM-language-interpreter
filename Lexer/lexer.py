from typing import Optional

from Lexer.interface import Lexer
from Source.source import SourceReader
from Source.source_position import SourcePosition
from Token.token import Token
from Token.token_type import TokenType
from Lexer.lexer_error import LexerError


class Lexer(Lexer):
    def __init__(self, source: SourceReader, currency_names: list = None, identifier_max_len=80,
                 str_max_len=120, int_max_len=15, float_max_len=30):
        self._source = source
        if currency_names is None:
            currency_names = []
        self._currencies = currency_names
        self._identifier_max_len = identifier_max_len
        self._str_max_len = str_max_len
        self._int_max_len = int_max_len
        self._float_max_len = float_max_len

    single_char_tokens = {
        "*": TokenType.MUL,
        "/": TokenType.DIV,
        ":": TokenType.COLON,
        "(": TokenType.LEFT_BRACKET,
        ")": TokenType.RIGHT_BRACKET,
        ".": TokenType.DOT,
        ",": TokenType.COMMA,
        "{": TokenType.LEFT_CURLY_BRACKET,
        "}": TokenType.RIGHT_CURLY_BRACKET,
        ";": TokenType.SEMICOLON
    }

    possible_double_char_tokens = {
        "+": TokenType.PLUS,
        "-": TokenType.MINUS,
        "<": TokenType.LESS,
        ">": TokenType.GREATER,
        "=": TokenType.ASSIGN,
        "!": TokenType.NOT
    }

    double_char_tokens = {
        "+=": TokenType.ADD_AND_ASSIGN,
        "-=": TokenType.SUB_AND_ASSIGN,
        "<=": TokenType.LESS_EQUAL,
        ">=": TokenType.GREATER_EQUAL,
        "==": TokenType.EQUAL,
        "!=": TokenType.NOT_EQUAL,
        "->": TokenType.CUR_TRANSFER
    }

    double_char_tokens_only = {
        "&&": TokenType.AND,
        "||": TokenType.OR
    }

    keywords = {
        "int": TokenType.INT,
        "float": TokenType.FLOAT,
        "str": TokenType.STR,
        "cur": TokenType.CUR,
        "curtype": TokenType.CURTYPE,
        "dict": TokenType.DICT,
        "bool": TokenType.BOOL,
        "void": TokenType.VOID,
        "true": TokenType.BOOL_VALUE_TRUE,
        "false": TokenType.BOOL_VALUE_FALSE,
        "if": TokenType.IF,
        "elif": TokenType.ELIF,
        "else": TokenType.ELSE,
        "while": TokenType.WHILE,
        "for": TokenType.FOR,
        "in": TokenType.IN,
        "from": TokenType.FROM,
        "return": TokenType.RETURN
    }

    def _get_char(self) -> str:
        return self._source.get_char()

    def _get_position(self) -> SourcePosition:
        return self._source.get_position()

    def _next_char(self):
        return self._source.next_char()

    def get_next_token(self):
        self._skip_whitespace()

        token = self._try_build_eof() \
            or self._try_build_comment() \
            or self._try_build_number() \
            or self._try_build_one_or_more_char_token() \
            or self._try_build_double_char_token() \
            or self._try_build_identifier_or_keyword_or_curtype_const() \
            or self._try_build_string()
        if token:
            return token

        raise LexerError("Can't match any token", self._get_position())

    def _skip_whitespace(self):
        char = self._get_char()

        while char.isspace():
            self._next_char()
            char = self._get_char()

    def _try_build_comment(self):
        char = self._get_char()

        if char != "#":
            return None

        result = []
        position = self._get_position()
        self._next_char()

        while self._get_char() != "\n" and self._get_char() != chr(3):
            result.append(self._get_char())
            self._next_char()

        self._next_char()
        return Token(TokenType.COMMENT, "".join(result), position)

    def _try_build_eof(self) -> Optional[Token]:
        if self._get_char() == chr(3):
            return Token(TokenType.END_OF_FILE, "", self._get_position())
        return None

    def _try_build_one_or_more_char_token(self) -> Optional[Token]:
        char = self._get_char()
        position = self._get_position()

        if token_type := self.single_char_tokens.get(char):
            self._next_char()
            return Token(token_type, "", position)

        elif token_type := self.possible_double_char_tokens.get(char):
            self._next_char()
            second_char = self._get_char()

            token = Token(self.double_char_tokens.get(char + second_char, token_type), "", position)

            if token.type in self.double_char_tokens.values():
                self._next_char()

            return token

        else:
            return None

    def _try_build_double_char_token(self) -> Optional[Token]:
        char = self._get_char()
        position = self._get_position()

        for operator in self.double_char_tokens_only:
            if char == operator[0]:
                self._next_char()
                second_char = self._get_char()
                if second_char == operator[1]:
                    self._next_char()
                    return Token(self.double_char_tokens_only[operator], "", position)
                else:
                    raise LexerError("Missing second char in double char token", position)

        return None

    def _try_build_identifier_or_keyword_or_curtype_const(self) -> Optional[Token]:
        char = self._get_char()

        if not char.isalpha():
            return None

        result_list = []
        position = self._get_position()

        while char.isalpha() or char.isdecimal() or char == "_":
            if len(result_list) == self._identifier_max_len:
                raise LexerError("Too many characters in identifier", position)
            result_list.append(char)
            self._next_char()
            char = self._get_char()

        result = "".join(result_list)
        if result in self.keywords:
            return Token(self.keywords[result], "", position)
        elif result.upper() in self._currencies:
            return Token(TokenType.CURTYPE_CONST, result.upper(), position)
        else:
            return Token(TokenType.IDENTIFIER, result, position)

    def _try_build_string(self) -> Optional[Token]:
        char = self._get_char()

        if char != '"':
            return None

        result = []
        position = self._get_position()

        self._next_char()
        char = self._get_char()

        while char != '"':
            if char == chr(3):
                raise LexerError("Can't match a token, unterminated string", position)
            if char == "\n":
                raise LexerError("Can't match a token, multiline string", position)
            char_to_append = self._handle_escape(char)
            if len(result) == self._str_max_len:
                raise LexerError("Max string length exceeded", position)

            result.append(char_to_append)
            self._next_char()
            char = self._get_char()

        self._next_char()
        return Token(TokenType.STR_CONST, "".join(result), position)

    def _try_build_number(self) -> Optional[Token]:
        char = self._get_char()

        if not char.isdecimal():
            return None

        number = 0
        position = self._get_position()

        if char == "0":
            self._next_char()
            char = self._get_char()
        else:
            while char.isdecimal():
                if len(str(number)) == self._int_max_len:
                    raise LexerError(f"Max int length exceeded ({self._int_max_len})", position)

                number = number * 10 + int(char)

                self._next_char()
                char = self._get_char()

        if token := self._build_float(number, position):
            return token
        else:
            return Token(TokenType.INT_CONST, number, position)

    def _build_float(self, number, position) -> Token:
        char = self._get_char()
        if char != ".":
            return None
        self._next_char()

        char = self._get_char()

        if not char.isdecimal():
            raise LexerError("No digit after '.' in a float number", position)

        decimals = 0
        i = 0

        while char.isdecimal():
            if len(str(decimals)) == self._float_max_len:
                raise LexerError(f"Max float length exceeded ({self._float_max_len})", position)
            i += 1

            decimals = decimals * 10 + int(char)
            self._next_char()
            char = self._get_char()

        number = number + decimals / 10**i

        return Token(TokenType.FLOAT_CONST, number, position)

    escape_characters = {
        '"': '"',
        "\\": "\\",
        "n": chr(10),
        "t": chr(9)
    }

    def _handle_escape(self, char):
        if char != "\\":
            return char

        self._next_char()
        char = self._get_char()
        return self.escape_characters.get(char, "\\" + char)


def generate_token(lexer: Lexer):
    while (new_token := lexer.get_next_token()).type != TokenType.END_OF_FILE:
        if new_token.type == TokenType.COMMENT:
            continue
        yield new_token

    yield new_token
