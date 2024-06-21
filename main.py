import sys

from Lexer.lexer import Lexer
from Source.source import SourceReader
from Lexer.exchange_rate_analyser import get_currency_types, get_exchange_rates
from Parser.parser import Parser
from Visitor.interpreter_visitor import InterpreterVisitor


if __name__ == '__main__':
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print('Expected one or two arguments: path_to_file [path_to_exchange_rate_file]')
        sys.exit()

    path_to_file = str(sys.argv[1])

    default_exchange_config_path = "eurofxref.csv"
    path_to_exchange_config = str(sys.argv[2]) if len(sys.argv) == 3 else default_exchange_config_path

    currencies = get_currency_types(path_to_exchange_config)
    exchange_rates = get_exchange_rates(path_to_exchange_config)

    with open(path_to_file, "r") as file:
        try:
            source = SourceReader(file)
            lexer = Lexer(source, currency_names=currencies)
            parser = Parser(lexer)
            program = parser.parse()
            interpreter = InterpreterVisitor(exchange_rates)
            program.accept(interpreter)
        except Exception as e:
            print(e)
            sys.exit()
