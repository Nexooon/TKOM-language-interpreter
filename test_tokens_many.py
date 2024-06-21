from Lexer.lexer import Lexer, generate_token
from Source.source import SourceReader
from Lexer.exchange_rate_analyser import get_currency_types


def var_init():
    currencies = get_currency_types("eurofxref.csv")
    currencies.append('EUR')

    file_path = "test_files/init.bng"
    with open(file_path, "r") as file:
        source = SourceReader(file)
        lexer = Lexer(source, currency_names=currencies)
        for token in generate_token(lexer):
            print(token)


def constructions():
    currencies = get_currency_types("eurofxref.csv")
    currencies.append('EUR')

    file_path = "test_files/some_constructions.bng"
    with open(file_path, "r") as file:
        source = SourceReader(file)
        lexer = Lexer(source, currency_names=currencies)
        for token in generate_token(lexer):
            print(token)


def currency():
    currencies = get_currency_types("eurofxref.csv")
    currencies.append('EUR')

    file_path = "test_files/currency.bng"
    with open(file_path, "r") as file:
        source = SourceReader(file)
        lexer = Lexer(source, currency_names=currencies)
        for token in generate_token(lexer):
            print(token)


var_init()
# constructions()
# currency()
