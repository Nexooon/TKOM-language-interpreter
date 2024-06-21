from Lexer.lexer import Lexer
from Lexer.lexer_error import LexerError
from Token.token_type import TokenType
from Source.source import SourceReader


class ExchangeRateAnalyser:
    def __init__(self, lexer: Lexer):
        self._lexer = lexer

    def get_currency_types(self):
        currencies = []

        while (token := self._lexer.get_next_token()).type == TokenType.IDENTIFIER:
            currencies.append(token.value)
            if (token := self._lexer.get_next_token()).type != TokenType.COMMA:
                raise LexerError("Wrong csv file format - missing coma.", token.position)

        return currencies

    def _get_types_and_rates(self):
        types = []
        rates = []

        while (token := self._lexer.get_next_token()).type == TokenType.IDENTIFIER:
            types.append(token.value)
            if (token := self._lexer.get_next_token()).type != TokenType.COMMA:
                raise LexerError("Wrong csv file format - missing coma.", token.position)

        while token.type == TokenType.FLOAT_CONST:
            rates.append(token.value)
            if (token := self._lexer.get_next_token()).type != TokenType.COMMA:
                raise LexerError("Wrong csv file format - missing coma.", token.position)
            token = self._lexer.get_next_token()

        if len(types) != len(rates):
            raise LexerError(
                "Expected same amount of currency types and exchange rates in an exchange rate csv file.",
                token.position
            )

        return types, rates

    def get_exchange_rates(self):
        exchange_rate = {}
        types, rates = self._get_types_and_rates()
        for type, rate in zip(types, rates):
            exchange_rate[type] = rate

        return exchange_rate


def get_currency_types(file_path):
    with open(file_path, "r") as file:
        source = SourceReader(file)
        lexer = Lexer(source)
        analyser = ExchangeRateAnalyser(lexer)
        return analyser.get_currency_types()


def get_exchange_rates(file_path):
    with open(file_path, "r") as file:
        source = SourceReader(file)
        lexer = Lexer(source)
        analyser = ExchangeRateAnalyser(lexer)
        return analyser.get_exchange_rates()
