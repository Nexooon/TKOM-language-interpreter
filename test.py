from Lexer.lexer import Lexer, generate_token
from Source.source import SourceReader
from Lexer.exchange_rate_analyser import get_currency_types, get_exchange_rates
from Parser.parser import Parser


def test_program():
    currencies = get_currency_types("eurofxref.csv")

    file_path = "test_files/program.bng"
    with open(file_path, "r") as file:
        source = SourceReader(file)
        lexer = Lexer(source, currency_names=currencies)
        parser = Parser(lexer)
        program = parser.parse_program()
        print(program.functions)


def constructions():
    currencies = get_currency_types("eurofxref.csv")

    file_path = "test_files/some_constructions.bng"
    with open(file_path, "r") as file:
        source = SourceReader(file)
        lexer = Lexer(source, currency_names=currencies)
        for token in generate_token(lexer):
            print(token)


def currency():
    currencies = get_currency_types("eurofxref.csv")
    rates = get_exchange_rates("eurofxref.csv")
    print(rates)

    file_path = "test_files/currency.bng"
    with open(file_path, "r") as file:
        source = SourceReader(file)
        lexer = Lexer(source, currency_names=currencies)
        for token in generate_token(lexer):
            print(token)


def test_1():
    currencies = get_currency_types("eurofxref.csv")

    file_path = "test_files/test1.bng"
    with open(file_path, "r") as file:
        source = SourceReader(file)
        lexer = Lexer(source, currency_names=currencies)
        parser = Parser(lexer)
        program = parser.parse_program()
        print(program.functions)


# test_program()
# constructions()
# currency()
test_1()
