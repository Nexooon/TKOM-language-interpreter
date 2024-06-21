import pytest
import io
from Lexer.lexer import Lexer
from Lexer.lexer_error import LexerError
from Token.token_type import TokenType
from Source.source_position import SourcePosition
from Source.source import SourceReader


@pytest.fixture
def lexer_str_setup(request):
    def _lexer_str_setup(string):
        source = SourceReader(io.StringIO(string))
        return Lexer(source)
    return _lexer_str_setup


def test_EOF(lexer_str_setup):
    lexer = lexer_str_setup("")
    token = lexer.get_next_token()
    assert token.type == TokenType.END_OF_FILE
    assert token.position == SourcePosition(1, 1)

    token = lexer.get_next_token()
    assert token.type == TokenType.END_OF_FILE
    assert token.position == SourcePosition(1, 1)


def test_new_line_EOF(lexer_str_setup):
    lexer = lexer_str_setup("\n")
    token = lexer.get_next_token()
    assert token.type == TokenType.END_OF_FILE
    assert token.position == SourcePosition(2, 1)

    token = lexer.get_next_token()
    assert token.type == TokenType.END_OF_FILE
    assert token.position == SourcePosition(2, 1)


def test_whitespace(lexer_str_setup):
    lexer = lexer_str_setup("  \n     ")
    token = lexer.get_next_token()
    assert token.type == TokenType.END_OF_FILE


def test_comment(lexer_str_setup):
    lexer = lexer_str_setup(" # komentarz ")
    token = lexer.get_next_token()
    assert token.type == TokenType.COMMENT
    assert token.position == SourcePosition(1, 2)


def test_comment2(lexer_str_setup):
    lexer = lexer_str_setup(" # komentarz \nint ")
    token = lexer.get_next_token()
    assert token.type == TokenType.COMMENT

    token = lexer.get_next_token()
    assert token.type == TokenType.INT


# single char tokens


def test_mul(lexer_str_setup):
    lexer = lexer_str_setup(" * ")
    token = lexer.get_next_token()
    assert token.type == TokenType.MUL
    assert token.position == SourcePosition(1, 2)


def test_div(lexer_str_setup):
    lexer = lexer_str_setup("  / ")
    token = lexer.get_next_token()
    assert token.type == TokenType.DIV
    assert token.position == SourcePosition(1, 3)


def test_colon(lexer_str_setup):
    lexer = lexer_str_setup(" : ")
    token = lexer.get_next_token()
    assert token.type == TokenType.COLON


def test_left_bracket(lexer_str_setup):
    lexer = lexer_str_setup(" ( ")
    token = lexer.get_next_token()
    assert token.type == TokenType.LEFT_BRACKET


def test_right_bracket(lexer_str_setup):
    lexer = lexer_str_setup(" ) ")
    token = lexer.get_next_token()
    assert token.type == TokenType.RIGHT_BRACKET


def test_dot(lexer_str_setup):
    lexer = lexer_str_setup(" . ")
    token = lexer.get_next_token()
    assert token.type == TokenType.DOT


def test_comma(lexer_str_setup):
    lexer = lexer_str_setup(" , ")
    token = lexer.get_next_token()
    assert token.type == TokenType.COMMA


def test_left_curly_bracket(lexer_str_setup):
    lexer = lexer_str_setup(" { ")
    token = lexer.get_next_token()
    assert token.type == TokenType.LEFT_CURLY_BRACKET


def test_right_curly_bracket(lexer_str_setup):
    lexer = lexer_str_setup(" } ")
    token = lexer.get_next_token()
    assert token.type == TokenType.RIGHT_CURLY_BRACKET


def test_semicolon(lexer_str_setup):
    lexer = lexer_str_setup(" ; ")
    token = lexer.get_next_token()
    assert token.type == TokenType.SEMICOLON


def test_error(lexer_str_setup):
    lexer = lexer_str_setup(" @ ")
    with pytest.raises(LexerError):
        lexer.get_next_token()

# one or more char tokens


def test_plus(lexer_str_setup):
    lexer = lexer_str_setup("+")
    token = lexer.get_next_token()
    assert token.type == TokenType.PLUS
    assert token.position == SourcePosition(1, 1)


def test_add_and_assign(lexer_str_setup):
    lexer = lexer_str_setup("+=")
    token = lexer.get_next_token()
    assert token.type == TokenType.ADD_AND_ASSIGN
    assert token.position == SourcePosition(1, 1)


def test_minus(lexer_str_setup):
    lexer = lexer_str_setup("-")
    token = lexer.get_next_token()
    assert token.type == TokenType.MINUS
    assert token.position == SourcePosition(1, 1)


def test_sub_and_assign(lexer_str_setup):
    lexer = lexer_str_setup("-=")
    token = lexer.get_next_token()
    assert token.type == TokenType.SUB_AND_ASSIGN
    assert token.position == SourcePosition(1, 1)


def test_less(lexer_str_setup):
    lexer = lexer_str_setup("<")
    token = lexer.get_next_token()
    assert token.type == TokenType.LESS
    assert token.position == SourcePosition(1, 1)


def test_less_equal(lexer_str_setup):
    lexer = lexer_str_setup("<=")
    token = lexer.get_next_token()
    assert token.type == TokenType.LESS_EQUAL
    assert token.position == SourcePosition(1, 1)


def test_greater(lexer_str_setup):
    lexer = lexer_str_setup(">")
    token = lexer.get_next_token()
    assert token.type == TokenType.GREATER
    assert token.position == SourcePosition(1, 1)


def test_greater_equal(lexer_str_setup):
    lexer = lexer_str_setup(">=")
    token = lexer.get_next_token()
    assert token.type == TokenType.GREATER_EQUAL
    assert token.position == SourcePosition(1, 1)


def test_relation_term(lexer_str_setup):
    lexer = lexer_str_setup("a >= 10")
    token = lexer.get_next_token()
    assert token.type == TokenType.IDENTIFIER
    assert token.position == SourcePosition(1, 1)
    token = lexer.get_next_token()
    assert token.type == TokenType.GREATER_EQUAL
    assert token.position == SourcePosition(1, 3)
    token = lexer.get_next_token()
    assert token.type == TokenType.INT_CONST
    assert token.position == SourcePosition(1, 6)


def test_assign(lexer_str_setup):
    lexer = lexer_str_setup("=")
    token = lexer.get_next_token()
    assert token.type == TokenType.ASSIGN
    assert token.position == SourcePosition(1, 1)


def test_equal(lexer_str_setup):
    lexer = lexer_str_setup("==")
    token = lexer.get_next_token()
    assert token.type == TokenType.EQUAL
    assert token.position == SourcePosition(1, 1)


def test_not(lexer_str_setup):
    lexer = lexer_str_setup("!")
    token = lexer.get_next_token()
    assert token.type == TokenType.NOT
    assert token.position == SourcePosition(1, 1)


def test_not_equal(lexer_str_setup):
    lexer = lexer_str_setup("!=")
    token = lexer.get_next_token()
    assert token.type == TokenType.NOT_EQUAL
    assert token.position == SourcePosition(1, 1)


def test_possible_double_char_token(lexer_str_setup):
    lexer = lexer_str_setup("!/")
    token = lexer.get_next_token()
    assert token.type == TokenType.NOT
    assert token.position == SourcePosition(1, 1)

    token = lexer.get_next_token()
    assert token.type == TokenType.DIV
    assert token.position == SourcePosition(1, 2)


# double char tokens

def test_and(lexer_str_setup):
    lexer = lexer_str_setup(" && ")
    token = lexer.get_next_token()
    assert token.type == TokenType.AND
    assert token.value == ""
    assert token.position == SourcePosition(1, 2)


def test_or(lexer_str_setup):
    lexer = lexer_str_setup(" || ")
    token = lexer.get_next_token()
    assert token.type == TokenType.OR
    assert token.value == ""
    assert token.position == SourcePosition(1, 2)


def test_or2(lexer_str_setup):
    lexer = lexer_str_setup(" || b")
    token = lexer.get_next_token()
    assert token.type == TokenType.OR
    assert token.value == ""
    assert token.position == SourcePosition(1, 2)

    token = lexer.get_next_token()
    assert token.type == TokenType.IDENTIFIER
    assert token.value == "b"
    assert token.position == SourcePosition(1, 5)


def test_and_error(lexer_str_setup):
    lexer = lexer_str_setup(" & ")
    with pytest.raises(LexerError):
        lexer.get_next_token()


def test_or_error(lexer_str_setup):
    lexer = lexer_str_setup(" ||| ")
    lexer.get_next_token()
    with pytest.raises(LexerError):
        lexer.get_next_token()


# keywords

def test_identifier(lexer_str_setup):
    lexer = lexer_str_setup(" my_name1 ")
    token = lexer.get_next_token()
    assert token.type == TokenType.IDENTIFIER
    assert token.position == SourcePosition(1, 2)
    assert token.value == "my_name1"


def test_identifier_polish(lexer_str_setup):
    lexer = lexer_str_setup(" mójTekst ")
    token = lexer.get_next_token()
    assert token.type == TokenType.IDENTIFIER
    assert token.position == SourcePosition(1, 2)
    assert token.value == "mójTekst"


def test_identifier_length():
    source = SourceReader(io.StringIO(" aaaa "))
    lexer = Lexer(source, identifier_max_len=4)
    token = lexer.get_next_token()
    assert token.value == "aaaa"

    source = SourceReader(io.StringIO(" aaaa "))
    lexer = Lexer(source, identifier_max_len=3)
    with pytest.raises(LexerError):
        lexer.get_next_token()


def test_int(lexer_str_setup):
    lexer = lexer_str_setup("  \nint ")
    token = lexer.get_next_token()
    assert token.type == TokenType.INT
    assert token.position == SourcePosition(2, 1)


def test_float(lexer_str_setup):
    lexer = lexer_str_setup(" float ")
    token = lexer.get_next_token()
    assert token.type == TokenType.FLOAT
    assert token.position == SourcePosition(1, 2)


def test_str(lexer_str_setup):
    lexer = lexer_str_setup(" str ")
    token = lexer.get_next_token()
    assert token.type == TokenType.STR
    assert token.position == SourcePosition(1, 2)


def test_cur(lexer_str_setup):
    lexer = lexer_str_setup(" cur ")
    token = lexer.get_next_token()
    assert token.type == TokenType.CUR
    assert token.position == SourcePosition(1, 2)


def test_curtype(lexer_str_setup):
    lexer = lexer_str_setup(" curtype ")
    token = lexer.get_next_token()
    assert token.type == TokenType.CURTYPE
    assert token.position == SourcePosition(1, 2)


def test_dict(lexer_str_setup):
    lexer = lexer_str_setup(" dict ")
    token = lexer.get_next_token()
    assert token.type == TokenType.DICT
    assert token.position == SourcePosition(1, 2)


def test_bool(lexer_str_setup):
    lexer = lexer_str_setup(" bool ")
    token = lexer.get_next_token()
    assert token.type == TokenType.BOOL
    assert token.position == SourcePosition(1, 2)


def test_void(lexer_str_setup):
    lexer = lexer_str_setup(" void ")
    token = lexer.get_next_token()
    assert token.type == TokenType.VOID
    assert token.position == SourcePosition(1, 2)


def test_if(lexer_str_setup):
    lexer = lexer_str_setup(" if ")
    token = lexer.get_next_token()
    assert token.type == TokenType.IF
    assert token.position == SourcePosition(1, 2)


def test_elif(lexer_str_setup):
    lexer = lexer_str_setup(" elif ")
    token = lexer.get_next_token()
    assert token.type == TokenType.ELIF
    assert token.position == SourcePosition(1, 2)


def test_else(lexer_str_setup):
    lexer = lexer_str_setup(" else ")
    token = lexer.get_next_token()
    assert token.type == TokenType.ELSE
    assert token.position == SourcePosition(1, 2)


def test_while(lexer_str_setup):
    lexer = lexer_str_setup(" while ")
    token = lexer.get_next_token()
    assert token.type == TokenType.WHILE
    assert token.position == SourcePosition(1, 2)


def test_for(lexer_str_setup):
    lexer = lexer_str_setup(" for ")
    token = lexer.get_next_token()
    assert token.type == TokenType.FOR
    assert token.position == SourcePosition(1, 2)


def test_in(lexer_str_setup):
    lexer = lexer_str_setup(" in ")
    token = lexer.get_next_token()
    assert token.type == TokenType.IN
    assert token.position == SourcePosition(1, 2)


def test_return(lexer_str_setup):
    lexer = lexer_str_setup(" return ")
    token = lexer.get_next_token()
    assert token.type == TokenType.RETURN
    assert token.position == SourcePosition(1, 2)


def test_from(lexer_str_setup):
    lexer = lexer_str_setup(" from ")
    token = lexer.get_next_token()
    assert token.type == TokenType.FROM
    assert token.position == SourcePosition(1, 2)


# consts

def test_str_const(lexer_str_setup):
    lexer = lexer_str_setup(' "abc" ')
    token = lexer.get_next_token()
    assert token.type == TokenType.STR_CONST
    assert token.position == SourcePosition(1, 2)
    assert token.value == "abc"


def test_str_const2(lexer_str_setup):
    lexer = lexer_str_setup(' "abc abc CDD" ')
    token = lexer.get_next_token()
    assert token.type == TokenType.STR_CONST
    assert token.position == SourcePosition(1, 2)
    assert token.value == "abc abc CDD"


# "ala
# ma kota"
def test_multiline_str_const(lexer_str_setup):
    lexer = lexer_str_setup('"ala\nma kota"')
    with pytest.raises(LexerError):
        lexer.get_next_token()


# "ala\nma kota"
def test_multiline_str_const2(lexer_str_setup):
    lexer = lexer_str_setup('"ala\\nma kota"')
    token = lexer.get_next_token()
    assert token.type == TokenType.STR_CONST
    assert token.position == SourcePosition(1, 1)
    assert token.value == "ala\nma kota"


def test_escaping_tab(lexer_str_setup):
    lexer = lexer_str_setup('"ala\\tma kota"')
    token = lexer.get_next_token()
    assert token.type == TokenType.STR_CONST
    assert token.position == SourcePosition(1, 1)
    assert token.value == "ala\tma kota"


def test_escaping_quote(lexer_str_setup):
    lexer = lexer_str_setup('"ala\\"ma kota"')
    token = lexer.get_next_token()
    assert token.type == TokenType.STR_CONST
    assert token.position == SourcePosition(1, 1)
    assert token.value == "ala\"ma kota"


def test_escaping_backslash(lexer_str_setup):
    lexer = lexer_str_setup('"ala\\\ma kota"')
    token = lexer.get_next_token()
    assert token.type == TokenType.STR_CONST
    assert token.position == SourcePosition(1, 1)
    assert token.value == "ala\\ma kota"


def test_not_escaping(lexer_str_setup):
    lexer = lexer_str_setup('"ala\\wma kota"')
    token = lexer.get_next_token()
    assert token.type == TokenType.STR_CONST
    assert token.position == SourcePosition(1, 1)
    assert token.value == "ala\\wma kota"


def test_str_const_length():
    source = SourceReader(io.StringIO(' "bbbb" '))
    lexer = Lexer(source, str_max_len=4)
    token = lexer.get_next_token()
    assert token.value == "bbbb"

    source = SourceReader(io.StringIO(' "bbbb" '))
    lexer = Lexer(source, str_max_len=3)
    with pytest.raises(LexerError):
        lexer.get_next_token()


def test_str_const_error2(lexer_str_setup):
    lexer = lexer_str_setup(' "ababab ')
    with pytest.raises(LexerError):
        lexer.get_next_token()

# numbers


def test_int_const(lexer_str_setup):
    lexer = lexer_str_setup(" 231 ")
    token = lexer.get_next_token()
    assert token.type == TokenType.INT_CONST
    assert token.position == SourcePosition(1, 2)
    assert token.value == 231


def test_int_const2(lexer_str_setup):
    lexer = lexer_str_setup(" 0 ")
    token = lexer.get_next_token()
    assert token.type == TokenType.INT_CONST
    assert token.position == SourcePosition(1, 2)
    assert token.value == 0


def test_int_const_negative(lexer_str_setup):
    lexer = lexer_str_setup(" -201 ")
    token = lexer.get_next_token()
    assert token.type == TokenType.MINUS
    assert token.position == SourcePosition(1, 2)

    token = lexer.get_next_token()
    assert token.type == TokenType.INT_CONST
    assert token.position == SourcePosition(1, 3)
    assert token.value == 201


def test_int_const_zero(lexer_str_setup):
    lexer = lexer_str_setup(" 021 ")
    token = lexer.get_next_token()
    assert token.type == TokenType.INT_CONST
    assert token.position == SourcePosition(1, 2)
    assert token.value == 0

    token = lexer.get_next_token()
    assert token.type == TokenType.INT_CONST
    assert token.position == SourcePosition(1, 3)
    assert token.value == 21


def test_int_const_length():
    source = SourceReader(io.StringIO(" 2024 "))
    lexer = Lexer(source, int_max_len=4)
    token = lexer.get_next_token()
    assert token.value == 2024

    source = SourceReader(io.StringIO(" 2024 "))
    lexer = Lexer(source, int_max_len=3)
    with pytest.raises(LexerError):
        lexer.get_next_token()


def test_int_const_length_negative():
    source = SourceReader(io.StringIO(" -2024 "))
    lexer = Lexer(source, int_max_len=4)
    lexer.get_next_token()
    token = lexer.get_next_token()
    assert token.value == 2024

    source = SourceReader(io.StringIO(" -2024 "))
    lexer = Lexer(source, int_max_len=3)
    lexer.get_next_token()
    with pytest.raises(LexerError):
        lexer.get_next_token()


def test_flaot_const(lexer_str_setup):
    lexer = lexer_str_setup(" 12.2342 ")
    token = lexer.get_next_token()
    assert token.type == TokenType.FLOAT_CONST
    assert token.position == SourcePosition(1, 2)
    assert token.value == 12.2342


def test_flaot_const2(lexer_str_setup):
    lexer = lexer_str_setup(" 0.01111 ")
    token = lexer.get_next_token()
    assert token.type == TokenType.FLOAT_CONST
    assert token.position == SourcePosition(1, 2)
    assert token.value == 0.01111


def test_flaot_const3(lexer_str_setup):
    lexer = lexer_str_setup(" 0.00023 ")
    token = lexer.get_next_token()
    assert token.type == TokenType.FLOAT_CONST
    assert token.position == SourcePosition(1, 2)
    assert token.value == 0.00023


def test_flaot_const4(lexer_str_setup):
    lexer = lexer_str_setup(" 0.1200 ")
    token = lexer.get_next_token()
    assert token.type == TokenType.FLOAT_CONST
    assert token.position == SourcePosition(1, 2)
    assert token.value == 0.12


def test_flaot_const_and_dot(lexer_str_setup):
    lexer = lexer_str_setup(" 0.12.3 ")
    token = lexer.get_next_token()
    assert token.type == TokenType.FLOAT_CONST
    assert token.position == SourcePosition(1, 2)
    assert token.value == 0.12

    token = lexer.get_next_token()
    assert token.type == TokenType.DOT
    assert token.position == SourcePosition(1, 6)

    token = lexer.get_next_token()
    assert token.type == TokenType.INT_CONST
    assert token.position == SourcePosition(1, 7)
    assert token.value == 3


def test_float_const_length():
    source = SourceReader(io.StringIO(" 2.2222 "))
    lexer = Lexer(source, float_max_len=4)
    token = lexer.get_next_token()
    assert token.value == 2.2222

    source = SourceReader(io.StringIO(" 2.2222 "))
    lexer = Lexer(source, float_max_len=3)
    with pytest.raises(LexerError):
        lexer.get_next_token()


def test_float_const_error2(lexer_str_setup):
    lexer = lexer_str_setup(" 2. ")
    with pytest.raises(LexerError):
        lexer.get_next_token()


def test_curtype_const():
    source = SourceReader(io.StringIO(" USD "))
    currencies = ["USD", "PLN"]
    lexer = Lexer(source, currencies)
    token = lexer.get_next_token()
    assert token.type == TokenType.CURTYPE_CONST
    assert token.position == SourcePosition(1, 2)
    assert token.value == "USD"


def test_curtype_const_error2(lexer_str_setup):
    lexer = lexer_str_setup(" $PLN ")
    with pytest.raises(LexerError):
        lexer.get_next_token()
