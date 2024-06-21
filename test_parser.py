import pytest

from Lexer.interface import Lexer
from Parser.parser import Parser, ParserError
from Token.token import Token
from Token.token_type import TokenType
from Source.source_position import SourcePosition
from Parse_objects.objects import DocumentObjectModel

from Parse_objects.objects import (
    OrExpression,
    AndExpression,
    EqualRelation,
    NegatedExpression,
    AddExpression,
    SubExpression,
    MulExpression,
    DivExpression,
    IntConst,
    FloatConst,
    CurConst,
    StrConst,
    BoolConst,
    CurtypeConst,
    Pair,
    DictConst,
    Block,
    AddAndAssign,
    SubAndAssign,
    Declaration,
    IfStatement,
    WhileLoopStatement,
    ForLoopStatement,
    ReturnStatement,
    CurrencyTransfer,
    ObjectAccess,
    Assignment,
    IdentifierExpression,
    FunctionCall,
    Parameter,
    FunctionDefinition,
)


class FakeLexer(Lexer):
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_index = 0

    def get_next_token(self):
        if self.current_index < len(self.tokens):
            token = self.tokens[self.current_index]
            self.current_index += 1
            return token
        else:
            return Token(type=TokenType.END_OF_FILE, value="", source_position=SourcePosition(line=0, column=0))


class TestParser:

    @pytest.mark.parametrize('tokens, expected_tree', [
        (
            [
                Token(value="int", source_position=SourcePosition(line=1, column=1), type=TokenType.INT),
                Token(value='fun', source_position=SourcePosition(line=1, column=5), type=TokenType.IDENTIFIER),
                Token(value='(', source_position=SourcePosition(line=1, column=9), type=TokenType.LEFT_BRACKET),
                Token(value=')', source_position=SourcePosition(line=1, column=10), type=TokenType.RIGHT_BRACKET),
                Token(value='{', source_position=SourcePosition(line=1, column=12), type=TokenType.LEFT_CURLY_BRACKET),
                Token(value='}', source_position=SourcePosition(line=1, column=14), type=TokenType.RIGHT_CURLY_BRACKET),
                Token(value="", source_position=SourcePosition(line=1, column=34), type=TokenType.END_OF_FILE),
            ],
            FunctionDefinition(
                position=SourcePosition(line=1, column=1),
                name='fun',
                type=DocumentObjectModel.INT,
                params=[],
                block=Block(position=SourcePosition(line=1, column=12), statements=[])
            )
        ),
        (
            [
                Token(value='void', source_position=SourcePosition(line=1, column=1), type=TokenType.VOID),
                Token(value='fun', source_position=SourcePosition(line=1, column=6), type=TokenType.IDENTIFIER),
                Token(value='(', source_position=SourcePosition(line=1, column=9), type=TokenType.LEFT_BRACKET),
                Token(value='int', source_position=SourcePosition(line=1, column=10), type=TokenType.INT),
                Token(value='x', source_position=SourcePosition(line=1, column=14), type=TokenType.IDENTIFIER),
                Token(value=')', source_position=SourcePosition(line=1, column=15), type=TokenType.RIGHT_BRACKET),
                Token(value='{', source_position=SourcePosition(line=1, column=16), type=TokenType.LEFT_CURLY_BRACKET),
                Token(value='}', source_position=SourcePosition(line=1, column=18), type=TokenType.RIGHT_CURLY_BRACKET),
                Token(value="", source_position=SourcePosition(line=1, column=34), type=TokenType.END_OF_FILE),
            ],
            FunctionDefinition(
                position=SourcePosition(line=1, column=1),
                name='fun',
                type=DocumentObjectModel.VOID,
                params=[Parameter(position=SourcePosition(line=1, column=10), name='x', type=DocumentObjectModel.INT)],
                block=Block(position=SourcePosition(line=1, column=16), statements=[])
            )
        ),
        (
            [
                Token(value='float', source_position=SourcePosition(line=1, column=1), type=TokenType.FLOAT),
                Token(value='fun', source_position=SourcePosition(line=1, column=7), type=TokenType.IDENTIFIER),
                Token(value='(', source_position=SourcePosition(line=1, column=10), type=TokenType.LEFT_BRACKET),
                Token(value='str', source_position=SourcePosition(line=1, column=11), type=TokenType.STR),
                Token(value='x', source_position=SourcePosition(line=1, column=15), type=TokenType.IDENTIFIER),
                Token(value=',', source_position=SourcePosition(line=1, column=16), type=TokenType.COMMA),
                Token(value='str', source_position=SourcePosition(line=1, column=18), type=TokenType.STR),
                Token(value='y', source_position=SourcePosition(line=1, column=23), type=TokenType.IDENTIFIER),
                Token(value=')', source_position=SourcePosition(line=1, column=24), type=TokenType.RIGHT_BRACKET),
                Token(value='{', source_position=SourcePosition(line=1, column=25), type=TokenType.LEFT_CURLY_BRACKET),
                Token(value='}', source_position=SourcePosition(line=1, column=26), type=TokenType.RIGHT_CURLY_BRACKET),
                Token(value="", source_position=SourcePosition(line=1, column=34), type=TokenType.END_OF_FILE),
            ],
            FunctionDefinition(
                position=SourcePosition(line=1, column=1),
                name='fun',
                type=DocumentObjectModel.FLOAT,
                params=[
                    Parameter(position=SourcePosition(line=1, column=11), name='x', type=DocumentObjectModel.STR),
                    Parameter(position=SourcePosition(line=1, column=18), name='y', type=DocumentObjectModel.STR)
                ],
                block=Block(position=SourcePosition(line=1, column=25), statements=[])
            )
        ),
    ])
    def test_parse_function_definition(self, tokens, expected_tree):
        lexer = FakeLexer(tokens)
        parser = Parser(lexer)
        functions = parser._parse_fun_def()
        assert functions == expected_tree

    @pytest.mark.parametrize('tokens, expected_params', [
        (
            [
                Token(value='int', source_position=SourcePosition(line=1, column=1), type=TokenType.INT),
                Token(value='x', source_position=SourcePosition(line=1, column=5), type=TokenType.IDENTIFIER),
            ],
            [
                Parameter(position=SourcePosition(line=1, column=1), name='x', type=DocumentObjectModel.INT)
            ]
        ),
        (
            [
                Token(value='float', source_position=SourcePosition(line=1, column=1), type=TokenType.FLOAT),
                Token(value='y', source_position=SourcePosition(line=1, column=7), type=TokenType.IDENTIFIER),
                Token(value=',', source_position=SourcePosition(line=1, column=8), type=TokenType.COMMA),
                Token(value='str', source_position=SourcePosition(line=1, column=10), type=TokenType.STR),
                Token(value='z', source_position=SourcePosition(line=1, column=14), type=TokenType.IDENTIFIER),
            ],
            [
                Parameter(position=SourcePosition(line=1, column=1), name='y', type=DocumentObjectModel.FLOAT),
                Parameter(position=SourcePosition(line=1, column=10), name='z', type=DocumentObjectModel.STR)
            ]
        ),
        (
            [
                Token(value='bool', source_position=SourcePosition(line=1, column=1), type=TokenType.BOOL),
                Token(value='flag', source_position=SourcePosition(line=1, column=6), type=TokenType.IDENTIFIER),
                Token(value=',', source_position=SourcePosition(line=1, column=10), type=TokenType.COMMA),
                Token(value='cur', source_position=SourcePosition(line=1, column=12), type=TokenType.CUR),
                Token(value='amount', source_position=SourcePosition(line=1, column=16), type=TokenType.IDENTIFIER),
                Token(value=',', source_position=SourcePosition(line=1, column=22), type=TokenType.COMMA),
                Token(value='curtype', source_position=SourcePosition(line=1, column=24), type=TokenType.CURTYPE),
                Token(value='type', source_position=SourcePosition(line=1, column=32), type=TokenType.IDENTIFIER),
            ],
            [
                Parameter(position=SourcePosition(line=1, column=1), name='flag', type=DocumentObjectModel.BOOL),
                Parameter(position=SourcePosition(line=1, column=12), name='amount', type=DocumentObjectModel.CUR),
                Parameter(position=SourcePosition(line=1, column=24), name='type', type=DocumentObjectModel.CURTYPE)
            ]
        ),
        (
            [
                Token(value="", source_position=SourcePosition(line=1, column=1), type=TokenType.END_OF_FILE),
            ],
            []
        ),
        # Nieprawidłowy parametr po przecinku
        (
            [
                Token(value='int', source_position=SourcePosition(line=1, column=1), type=TokenType.INT),
                Token(value='x', source_position=SourcePosition(line=1, column=5), type=TokenType.IDENTIFIER),
                Token(value=',', source_position=SourcePosition(line=1, column=6), type=TokenType.COMMA),
                Token(value=',', source_position=SourcePosition(line=1, column=7), type=TokenType.COMMA),
            ],
            ParserError("Expected a parameter after \",\"", SourcePosition(line=1, column=7))
        ),
        # Pusty zestaw parametrów w środku
        (
            [
                Token(value='int', source_position=SourcePosition(line=1, column=1), type=TokenType.INT),
                Token(value='x', source_position=SourcePosition(line=1, column=5), type=TokenType.IDENTIFIER),
                Token(value=',', source_position=SourcePosition(line=1, column=6), type=TokenType.COMMA),
                Token(value=',', source_position=SourcePosition(line=1, column=7), type=TokenType.COMMA),
                Token(value='int', source_position=SourcePosition(line=1, column=8), type=TokenType.INT),
                Token(value='y', source_position=SourcePosition(line=1, column=12), type=TokenType.IDENTIFIER),
            ],
            ParserError("Expected a parameter after \",\"", SourcePosition(line=1, column=7))
        ),
        # Nieprawidłowy typ parametru
        (
            [
                Token(value='void', source_position=SourcePosition(line=1, column=1), type=TokenType.VOID),
                Token(value='x', source_position=SourcePosition(line=1, column=8), type=TokenType.IDENTIFIER),
            ],
            []
        ),
    ])
    def test_parse_parameters(self, tokens, expected_params):
        lexer = FakeLexer(tokens)
        parser = Parser(lexer)
        if isinstance(expected_params, ParserError):
            with pytest.raises(ParserError) as excinfo:
                parser._parse_parameters()
            assert excinfo.value.message == expected_params.message
            assert excinfo.value.position == expected_params.position
        else:
            params = parser._parse_parameters()
            assert params == expected_params

    @pytest.mark.parametrize('tokens, expected_param', [
        # Prawidłowy pojedynczy parametr
        (
            [
                Token(value='int', source_position=SourcePosition(line=1, column=1), type=TokenType.INT),
                Token(value='x', source_position=SourcePosition(line=1, column=5), type=TokenType.IDENTIFIER),
            ],
            Parameter(position=SourcePosition(line=1, column=1), name='x', type=DocumentObjectModel.INT)
        ),
        # Prawidłowy pojedynczy parametr typu float
        (
            [
                Token(value='float', source_position=SourcePosition(line=1, column=1), type=TokenType.FLOAT),
                Token(value='y', source_position=SourcePosition(line=1, column=7), type=TokenType.IDENTIFIER),
            ],
            Parameter(position=SourcePosition(line=1, column=1), name='y', type=DocumentObjectModel.FLOAT)
        ),
        # Nieprawidłowy typ parametru
        (
            [
                Token(value='void', source_position=SourcePosition(line=1, column=1), type=TokenType.VOID),
                Token(value='z', source_position=SourcePosition(line=1, column=8), type=TokenType.IDENTIFIER),
            ],
            None  # Funkcja powinna zwrócić None
        ),
        # Brak identyfikatora po typie
        (
            [
                Token(value='int', source_position=SourcePosition(line=1, column=1), type=TokenType.INT),
                Token(value='', source_position=SourcePosition(line=1, column=5), type=TokenType.END_OF_FILE),
            ],
            ParserError("Expected IDENTIFIER, got END_OF_FILE", SourcePosition(line=1, column=5))
        ),
        # Brakujący identyfikator po typie cur
        (
            [
                Token(value='cur', source_position=SourcePosition(line=1, column=1), type=TokenType.CUR),
                Token(value='', source_position=SourcePosition(line=1, column=5), type=TokenType.END_OF_FILE),
            ],
            ParserError("Expected IDENTIFIER, got END_OF_FILE", SourcePosition(line=1, column=5))
        ),
        # Prawidłowy parametr typu bool
        (
            [
                Token(value='bool', source_position=SourcePosition(line=1, column=1), type=TokenType.BOOL),
                Token(value='flag', source_position=SourcePosition(line=1, column=6), type=TokenType.IDENTIFIER),
            ],
            Parameter(position=SourcePosition(line=1, column=1), name='flag', type=DocumentObjectModel.BOOL)
        ),
    ])
    def test_parse_parameter(self, tokens, expected_param):
        lexer = FakeLexer(tokens)
        parser = Parser(lexer)
        if isinstance(expected_param, ParserError):
            with pytest.raises(ParserError) as excinfo:
                parser._parse_parameter()
            assert excinfo.value.message == expected_param.message
            assert excinfo.value.position == expected_param.position
        elif expected_param is None:
            param = parser._parse_parameter()
            assert param is None
        else:
            param = parser._parse_parameter()
            assert param == expected_param

    @pytest.mark.parametrize('tokens, expected_block', [
        # Prawidłowy pusty blok
        (
            [
                Token(value='{', source_position=SourcePosition(line=1, column=1), type=TokenType.LEFT_CURLY_BRACKET),
                Token(value='}', source_position=SourcePosition(line=1, column=2), type=TokenType.RIGHT_CURLY_BRACKET),
            ],
            Block(position=SourcePosition(line=1, column=1), statements=[])
        ),
        # Blok z jednym prawidłowym statementem
        (
            [
                Token(value='{', source_position=SourcePosition(line=1, column=1), type=TokenType.LEFT_CURLY_BRACKET),
                Token(value='int', source_position=SourcePosition(line=2, column=1), type=TokenType.INT),
                Token(value='x', source_position=SourcePosition(line=2, column=5), type=TokenType.IDENTIFIER),
                Token(value=';', source_position=SourcePosition(line=2, column=6), type=TokenType.SEMICOLON),
                Token(value='}', source_position=SourcePosition(line=3, column=1), type=TokenType.RIGHT_CURLY_BRACKET),
            ],
            Block(position=SourcePosition(line=1, column=1), statements=[
                Declaration(
                    position=SourcePosition(line=2, column=1),
                    type=DocumentObjectModel.INT,
                    name='x'
                )
            ])
        ),
        # Blok z dwoma prawidłowymi statementami
        (
            [
                Token(value='{', source_position=SourcePosition(line=1, column=1), type=TokenType.LEFT_CURLY_BRACKET),
                Token(value='int', source_position=SourcePosition(line=2, column=1), type=TokenType.INT),
                Token(value='x', source_position=SourcePosition(line=2, column=5), type=TokenType.IDENTIFIER),
                Token(value=';', source_position=SourcePosition(line=2, column=6), type=TokenType.SEMICOLON),
                Token(value='x', source_position=SourcePosition(line=3, column=1), type=TokenType.IDENTIFIER),
                Token(value='=', source_position=SourcePosition(line=3, column=3), type=TokenType.ASSIGN),
                Token(value=10, source_position=SourcePosition(line=3, column=5), type=TokenType.INT_CONST),
                Token(value=';', source_position=SourcePosition(line=3, column=7), type=TokenType.SEMICOLON),
                Token(value='}', source_position=SourcePosition(line=4, column=1), type=TokenType.RIGHT_CURLY_BRACKET),
            ],
            Block(position=SourcePosition(line=1, column=1), statements=[
                Declaration(
                    position=SourcePosition(line=2, column=1),
                    type=DocumentObjectModel.INT,
                    name='x'
                ),
                Assignment(
                    position=SourcePosition(line=3, column=1),
                    object=ObjectAccess(
                        position=SourcePosition(line=3, column=1),
                        objects=[IdentifierExpression(
                            position=SourcePosition(line=3, column=1),
                            name='x'
                        )]
                    ),
                    expression=IntConst(
                        position=SourcePosition(line=3, column=5),
                        value=10
                    )
                )
            ])
        ),
        # Blok bez zamykającej klamry
        (
            [
                Token(value='{', source_position=SourcePosition(line=1, column=1), type=TokenType.LEFT_CURLY_BRACKET),
                Token(value='int', source_position=SourcePosition(line=2, column=1), type=TokenType.INT),
                Token(value='x', source_position=SourcePosition(line=2, column=5), type=TokenType.IDENTIFIER),
                Token(value=';', source_position=SourcePosition(line=2, column=6), type=TokenType.SEMICOLON),
                Token(value='', source_position=SourcePosition(line=2, column=7), type=TokenType.END_OF_FILE),
            ],
            ParserError("Expected RIGHT_CURLY_BRACKET, got END_OF_FILE", SourcePosition(line=2, column=7))
        ),
        # Blok z nieprawidłowym statementem
        (
            [
                Token(value='{', source_position=SourcePosition(line=1, column=1), type=TokenType.LEFT_CURLY_BRACKET),
                Token(value='.', source_position=SourcePosition(line=2, column=1), type=TokenType.DOT),
                Token(value='}', source_position=SourcePosition(line=3, column=1), type=TokenType.RIGHT_CURLY_BRACKET),
            ],
            ParserError("Expected RIGHT_CURLY_BRACKET, got DOT", SourcePosition(line=2, column=1))
        ),
    ])
    def test_parse_block(self, tokens, expected_block):
        lexer = FakeLexer(tokens)
        parser = Parser(lexer)
        if isinstance(expected_block, ParserError):
            with pytest.raises(ParserError) as excinfo:
                parser._parse_block()
            assert excinfo.value.message == expected_block.message
            assert excinfo.value.position == expected_block.position
        else:
            block = parser._parse_block()
            assert block == expected_block

    @pytest.mark.parametrize('tokens, expected_statement', [
        (
            [
                Token(value='{', source_position=SourcePosition(line=1, column=1), type=TokenType.LEFT_CURLY_BRACKET),
                Token(value='}', source_position=SourcePosition(line=1, column=2), type=TokenType.RIGHT_CURLY_BRACKET),
            ],
            None
        ),
    ])
    def test_parse_statement(self, tokens, expected_statement):
        lexer = FakeLexer(tokens)
        parser = Parser(lexer)
        if expected_statement is None:
            statement = parser._parse_statement()
            assert statement is None

    @pytest.mark.parametrize('tokens, expected_declaration', [
        # Prawidłowa deklaracja bez przypisania
        (
            [
                Token(value='int', source_position=SourcePosition(line=1, column=1), type=TokenType.INT),
                Token(value='x', source_position=SourcePosition(line=1, column=5), type=TokenType.IDENTIFIER),
                Token(value=';', source_position=SourcePosition(line=1, column=6), type=TokenType.SEMICOLON),
            ],
            Declaration(
                position=SourcePosition(line=1, column=1),
                type=DocumentObjectModel.INT,
                name='x'
            )
        ),
        # Prawidłowa deklaracja z przypisaniem
        (
            [
                Token(value='int', source_position=SourcePosition(line=1, column=1), type=TokenType.INT),
                Token(value='y', source_position=SourcePosition(line=1, column=5), type=TokenType.IDENTIFIER),
                Token(value='=', source_position=SourcePosition(line=1, column=6), type=TokenType.ASSIGN),
                Token(value=10, source_position=SourcePosition(line=1, column=8), type=TokenType.INT_CONST),
                Token(value=';', source_position=SourcePosition(line=1, column=10), type=TokenType.SEMICOLON),
            ],
            Assignment(
                position=SourcePosition(line=1, column=1),
                object=Declaration(
                    position=SourcePosition(line=1, column=1),
                    type=DocumentObjectModel.INT,
                    name='y'
                ),
                expression=IntConst(
                    position=SourcePosition(line=1, column=8),
                    value=10
                )
            )
        ),
        # Nieprawidłowy typ
        (
            [
                Token(value='void', source_position=SourcePosition(line=1, column=1), type=TokenType.VOID),
                Token(value='z', source_position=SourcePosition(line=1, column=8), type=TokenType.IDENTIFIER),
                Token(value=';', source_position=SourcePosition(line=1, column=9), type=TokenType.SEMICOLON),
            ],
            None
        ),
        # Brak identyfikatora po typie
        (
            [
                Token(value='int', source_position=SourcePosition(line=1, column=1), type=TokenType.INT),
                Token(value=';', source_position=SourcePosition(line=1, column=5), type=TokenType.SEMICOLON),
            ],
            ParserError("Expected IDENTIFIER, got SEMICOLON", SourcePosition(line=1, column=5))
        ),
        # Brakujący średnik po deklaracji
        (
            [
                Token(value='int', source_position=SourcePosition(line=1, column=1), type=TokenType.INT),
                Token(value='x', source_position=SourcePosition(line=1, column=5), type=TokenType.IDENTIFIER),
                Token(value='=', source_position=SourcePosition(line=1, column=6), type=TokenType.ASSIGN),
                Token(value=10, source_position=SourcePosition(line=1, column=8), type=TokenType.INT_CONST),
                Token(value='', source_position=SourcePosition(line=1, column=9), type=TokenType.END_OF_FILE),
            ],
            ParserError("Expected SEMICOLON, got END_OF_FILE", SourcePosition(line=1, column=9))
        ),
    ])
    def test_parse_declaration(self, tokens, expected_declaration):
        lexer = FakeLexer(tokens)
        parser = Parser(lexer)
        if isinstance(expected_declaration, ParserError):
            with pytest.raises(ParserError) as excinfo:
                parser._parse_declaration()
            assert excinfo.value.message == expected_declaration.message
            assert excinfo.value.position == expected_declaration.position
        elif expected_declaration is None:
            declaration = parser._parse_declaration()
            assert declaration is None
        else:
            declaration = parser._parse_declaration()
            assert declaration == expected_declaration

    @pytest.mark.parametrize('tokens, declaration, position, expected_assignment', [
        # Prawidłowe przypisanie wartości po deklaracji
        (
            [
                Token(value='=', source_position=SourcePosition(line=1, column=6), type=TokenType.ASSIGN),
                Token(value=10, source_position=SourcePosition(line=1, column=8), type=TokenType.INT_CONST),
                Token(value=';', source_position=SourcePosition(line=1, column=10), type=TokenType.SEMICOLON),
            ],
            Declaration(
                position=SourcePosition(line=1, column=1),
                type=DocumentObjectModel.INT,
                name='x'
            ),
            SourcePosition(line=1, column=1),
            Assignment(
                position=SourcePosition(line=1, column=1),
                object=Declaration(
                    position=SourcePosition(line=1, column=1),
                    type=DocumentObjectModel.INT,
                    name='x'
                ),
                expression=IntConst(
                    position=SourcePosition(line=1, column=8),
                    value=10
                )
            )
        ),
        # Brak przypisania
        (
            [
                Token(value=';', source_position=SourcePosition(line=1, column=6), type=TokenType.SEMICOLON),
            ],
            Declaration(
                position=SourcePosition(line=1, column=1),
                type=DocumentObjectModel.INT,
                name='x'
            ),
            SourcePosition(line=1, column=1),
            None
        ),
        # Brak wyrażenia po ASSIGN
        (
            [
                Token(value='=', source_position=SourcePosition(line=1, column=6), type=TokenType.ASSIGN),
                Token(value=';', source_position=SourcePosition(line=1, column=7), type=TokenType.SEMICOLON),
            ],
            Declaration(
                position=SourcePosition(line=1, column=1),
                type=DocumentObjectModel.INT,
                name='x'
            ),
            SourcePosition(line=1, column=1),
            ParserError("Expected an expression after \"=\".", SourcePosition(line=1, column=7))
        ),
        # Nieprawidłowe wyrażenie po ASSIGN
        (
            [
                Token(value='=', source_position=SourcePosition(line=1, column=6), type=TokenType.ASSIGN),
                Token(value='.', source_position=SourcePosition(line=1, column=8), type=TokenType.DOT),
                Token(value=';', source_position=SourcePosition(line=1, column=9), type=TokenType.SEMICOLON),
            ],
            Declaration(
                position=SourcePosition(line=1, column=1),
                type=DocumentObjectModel.INT,
                name='x'
            ),
            SourcePosition(line=1, column=1),
            ParserError("Expected an expression after \"=\".", SourcePosition(line=1, column=8))
        ),
    ])
    def test_parse_assign_declaration(self, tokens, declaration, position, expected_assignment):
        lexer = FakeLexer(tokens)
        parser = Parser(lexer)
        if isinstance(expected_assignment, ParserError):
            with pytest.raises(ParserError) as excinfo:
                parser._parse_assign_declaration(declaration, position)
            assert excinfo.value.message == expected_assignment.message
            assert excinfo.value.position == expected_assignment.position
        elif expected_assignment is None:
            assignment = parser._parse_assign_declaration(declaration, position)
            assert assignment is None
        else:
            assignment = parser._parse_assign_declaration(declaration, position)
            assert assignment == expected_assignment

    @pytest.mark.parametrize('tokens, expected_statement', [
        # Prawidłowe przypisanie wartości
        (
            [
                Token(value='x', source_position=SourcePosition(line=1, column=1), type=TokenType.IDENTIFIER),
                Token(value='=', source_position=SourcePosition(line=1, column=2), type=TokenType.ASSIGN),
                Token(value=10, source_position=SourcePosition(line=1, column=4), type=TokenType.INT_CONST),
                Token(value=';', source_position=SourcePosition(line=1, column=6), type=TokenType.SEMICOLON),
            ],
            Assignment(
                position=SourcePosition(line=1, column=1),
                object=ObjectAccess(
                    position=SourcePosition(line=1, column=1),
                    objects=[IdentifierExpression(
                        position=SourcePosition(line=1, column=1),
                        name='x'
                    )]
                ),
                expression=IntConst(
                    position=SourcePosition(line=1, column=4),
                    value=10
                )
            )
        ),
        # Prawidłowe przypisanie z dodaniem
        (
            [
                Token(value='x', source_position=SourcePosition(line=1, column=1), type=TokenType.IDENTIFIER),
                Token(value='+=', source_position=SourcePosition(line=1, column=2), type=TokenType.ADD_AND_ASSIGN),
                Token(value=10, source_position=SourcePosition(line=1, column=4), type=TokenType.INT_CONST),
                Token(value=';', source_position=SourcePosition(line=1, column=6), type=TokenType.SEMICOLON),
            ],
            AddAndAssign(
                position=SourcePosition(line=1, column=1),
                object=ObjectAccess(
                    position=SourcePosition(line=1, column=1),
                    objects=[IdentifierExpression(
                        position=SourcePosition(line=1, column=1),
                        name='x'
                    )]
                ),
                expression=IntConst(
                    position=SourcePosition(line=1, column=4),
                    value=10
                )
            )
        ),
        # Prawidłowe przypisanie z odejmowaniem
        (
            [
                Token(value='x', source_position=SourcePosition(line=1, column=1), type=TokenType.IDENTIFIER),
                Token(value='-=', source_position=SourcePosition(line=1, column=2), type=TokenType.SUB_AND_ASSIGN),
                Token(value=10, source_position=SourcePosition(line=1, column=4), type=TokenType.INT_CONST),
                Token(value=';', source_position=SourcePosition(line=1, column=6), type=TokenType.SEMICOLON),
            ],
            SubAndAssign(
                position=SourcePosition(line=1, column=1),
                object=ObjectAccess(
                    position=SourcePosition(line=1, column=1),
                    objects=[IdentifierExpression(
                        position=SourcePosition(line=1, column=1),
                        name='x'
                    )]
                ),
                expression=IntConst(
                    position=SourcePosition(line=1, column=4),
                    value=10
                )
            )
        ),
        # Wywołanie funkcji bez przypisania
        (
            [
                Token(value='fun', source_position=SourcePosition(line=1, column=1), type=TokenType.IDENTIFIER),
                Token(value='(', source_position=SourcePosition(line=1, column=4), type=TokenType.LEFT_BRACKET),
                Token(value=')', source_position=SourcePosition(line=1, column=5), type=TokenType.RIGHT_BRACKET),
                Token(value=';', source_position=SourcePosition(line=1, column=6), type=TokenType.SEMICOLON),
            ],
            ObjectAccess(
                position=SourcePosition(line=1, column=1),
                objects=[FunctionCall(
                    position=SourcePosition(line=1, column=1),
                    name='fun',
                    arguments=[]
                )]
            )
        ),
        # Brakujący średnik
        (
            [
                Token(value='x', source_position=SourcePosition(line=1, column=1), type=TokenType.IDENTIFIER),
                Token(value='=', source_position=SourcePosition(line=1, column=2), type=TokenType.ASSIGN),
                Token(value=10, source_position=SourcePosition(line=1, column=4), type=TokenType.INT_CONST),
                Token(value='', source_position=SourcePosition(line=1, column=5), type=TokenType.END_OF_FILE),
            ],
            ParserError("Expected SEMICOLON, got END_OF_FILE", SourcePosition(line=1, column=5))
        ),
        # Brak przypisania po identyfikatorze
        (
            [
                Token(value='x', source_position=SourcePosition(line=1, column=1), type=TokenType.IDENTIFIER),
                Token(value=';', source_position=SourcePosition(line=1, column=2), type=TokenType.SEMICOLON),
            ],
            ParserError("Expected assignment after identifier.", SourcePosition(line=1, column=1))
        ),
    ])
    def test_parse_assignment_or_function_call(self, tokens, expected_statement):
        lexer = FakeLexer(tokens)
        parser = Parser(lexer)
        if isinstance(expected_statement, ParserError):
            with pytest.raises(ParserError) as excinfo:
                parser._parse_assignment_or_function_call()
            assert excinfo.value.message == expected_statement.message
            assert excinfo.value.position == expected_statement.position
        else:
            statement = parser._parse_assignment_or_function_call()
            assert statement == expected_statement

    @pytest.mark.parametrize('tokens, object_access, position, expected_assignment', [
        # Prawidłowe przypisanie wartości
        (
            [
                Token(value='=', source_position=SourcePosition(line=1, column=2), type=TokenType.ASSIGN),
                Token(value=10, source_position=SourcePosition(line=1, column=4), type=TokenType.INT_CONST),
            ],
            ObjectAccess(
                position=SourcePosition(line=1, column=1),
                objects=[IdentifierExpression(
                    position=SourcePosition(line=1, column=1),
                    name='x'
                )]
            ),
            SourcePosition(line=1, column=1),
            Assignment(
                position=SourcePosition(line=1, column=1),
                object=ObjectAccess(
                    position=SourcePosition(line=1, column=1),
                    objects=[IdentifierExpression(
                        position=SourcePosition(line=1, column=1),
                        name='x'
                    )]
                ),
                expression=IntConst(
                    position=SourcePosition(line=1, column=4),
                    value=10
                )
            )
        ),
        # Prawidłowe przypisanie z dodaniem
        (
            [
                Token(value='+=', source_position=SourcePosition(line=1, column=2), type=TokenType.ADD_AND_ASSIGN),
                Token(value=10, source_position=SourcePosition(line=1, column=4), type=TokenType.INT_CONST),
            ],
            ObjectAccess(
                position=SourcePosition(line=1, column=1),
                objects=[IdentifierExpression(
                    position=SourcePosition(line=1, column=1),
                    name='x'
                )]
            ),
            SourcePosition(line=1, column=1),
            AddAndAssign(
                position=SourcePosition(line=1, column=1),
                object=ObjectAccess(
                    position=SourcePosition(line=1, column=1),
                    objects=[IdentifierExpression(
                        position=SourcePosition(line=1, column=1),
                        name='x'
                    )]
                ),
                expression=IntConst(
                    position=SourcePosition(line=1, column=4),
                    value=10
                )
            )
        ),
        # Prawidłowe przypisanie z odejmowaniem
        (
            [
                Token(value='-=', source_position=SourcePosition(line=1, column=2), type=TokenType.SUB_AND_ASSIGN),
                Token(value=10, source_position=SourcePosition(line=1, column=4), type=TokenType.INT_CONST),
            ],
            ObjectAccess(
                position=SourcePosition(line=1, column=1),
                objects=[IdentifierExpression(
                    position=SourcePosition(line=1, column=1),
                    name='x'
                )]
            ),
            SourcePosition(line=1, column=1),
            SubAndAssign(
                position=SourcePosition(line=1, column=1),
                object=ObjectAccess(
                    position=SourcePosition(line=1, column=1),
                    objects=[IdentifierExpression(
                        position=SourcePosition(line=1, column=1),
                        name='x'
                    )]
                ),
                expression=IntConst(
                    position=SourcePosition(line=1, column=4),
                    value=10
                )
            )
        ),
        # Przypisanie do wywołania funkcji (błąd)
        (
            [
                Token(value='=', source_position=SourcePosition(line=1, column=2), type=TokenType.ASSIGN),
                Token(value=10, source_position=SourcePosition(line=1, column=4), type=TokenType.INT_CONST),
            ],
            ObjectAccess(
                position=SourcePosition(line=1, column=1),
                objects=[FunctionCall(
                    position=SourcePosition(line=1, column=1),
                    name='fun',
                    arguments=[]
                )]
            ),
            SourcePosition(line=1, column=1),
            ParserError("Can't assign to function call", SourcePosition(line=1, column=1))
        ),
        # Brak wyrażenia po operatorze przypisania (błąd)
        (
            [
                Token(value='=', source_position=SourcePosition(line=1, column=2), type=TokenType.ASSIGN),
                Token(value=';', source_position=SourcePosition(line=1, column=4), type=TokenType.SEMICOLON),
            ],
            ObjectAccess(
                position=SourcePosition(line=1, column=1),
                objects=[IdentifierExpression(
                    position=SourcePosition(line=1, column=1),
                    name='x'
                )]
            ),
            SourcePosition(line=1, column=1),
            ParserError("Expected an expression after assignment operation.", SourcePosition(line=1, column=4))
        ),
        # Brak operatora przypisania (zwraca None)
        (
            [
                Token(value=';', source_position=SourcePosition(line=1, column=2), type=TokenType.SEMICOLON),
            ],
            ObjectAccess(
                position=SourcePosition(line=1, column=1),
                objects=[IdentifierExpression(
                    position=SourcePosition(line=1, column=1),
                    name='x'
                )]
            ),
            SourcePosition(line=1, column=1),
            None
        ),
    ])
    def test_parse_object_assignment(self, tokens, object_access, position, expected_assignment):
        lexer = FakeLexer(tokens)
        parser = Parser(lexer)
        if isinstance(expected_assignment, ParserError):
            with pytest.raises(ParserError) as excinfo:
                parser._parse_object_assignment(object_access, position)
            assert excinfo.value.message == expected_assignment.message
            assert excinfo.value.position == expected_assignment.position
        elif expected_assignment is None:
            assignment = parser._parse_object_assignment(object_access, position)
            assert assignment is None
        else:
            assignment = parser._parse_object_assignment(object_access, position)
            assert assignment == expected_assignment

    @pytest.mark.parametrize('tokens, expected_conditional', [
        # Prosty if bez elif i else
        (
            [
                Token(value='if', source_position=SourcePosition(line=1, column=1), type=TokenType.IF),
                Token(value='true', source_position=SourcePosition(line=1, column=4), type=TokenType.BOOL_VALUE_TRUE),
                Token(value='{', source_position=SourcePosition(line=1, column=9), type=TokenType.LEFT_CURLY_BRACKET),
                Token(value='}', source_position=SourcePosition(line=1, column=10), type=TokenType.RIGHT_CURLY_BRACKET),
            ],
            IfStatement(
                position=SourcePosition(line=1, column=1),
                condition=BoolConst(position=SourcePosition(line=1, column=4), value=True),
                block=Block(position=SourcePosition(line=1, column=9), statements=[]),
                elif_blocks=[],
                else_block=None
            )
        ),
        # if z jednym elif i bez else
        (
            [
                Token(value='if', source_position=SourcePosition(line=1, column=1), type=TokenType.IF),
                Token(value='true', source_position=SourcePosition(line=1, column=4), type=TokenType.BOOL_VALUE_TRUE),
                Token(value='{', source_position=SourcePosition(line=1, column=9), type=TokenType.LEFT_CURLY_BRACKET),
                Token(value='}', source_position=SourcePosition(line=1, column=10), type=TokenType.RIGHT_CURLY_BRACKET),
                Token(value='elif', source_position=SourcePosition(line=2, column=1), type=TokenType.ELIF),
                Token(value='false', source_position=SourcePosition(line=2, column=6), type=TokenType.BOOL_VALUE_FALSE),
                Token(value='{', source_position=SourcePosition(line=2, column=12), type=TokenType.LEFT_CURLY_BRACKET),
                Token(value='}', source_position=SourcePosition(line=2, column=13), type=TokenType.RIGHT_CURLY_BRACKET),
            ],
            IfStatement(
                position=SourcePosition(line=1, column=1),
                condition=BoolConst(position=SourcePosition(line=1, column=4), value=True),
                block=Block(position=SourcePosition(line=1, column=9), statements=[]),
                elif_blocks=[
                    (BoolConst(position=SourcePosition(line=2, column=6), value=False),
                     Block(position=SourcePosition(line=2, column=12), statements=[]))
                ],
                else_block=None
            )
        ),
        # if z dwoma elif i bez else
        (
            [
                Token(value='if', source_position=SourcePosition(line=1, column=1), type=TokenType.IF),
                Token(value='true', source_position=SourcePosition(line=1, column=4), type=TokenType.BOOL_VALUE_TRUE),
                Token(value='{', source_position=SourcePosition(line=1, column=9), type=TokenType.LEFT_CURLY_BRACKET),
                Token(value='}', source_position=SourcePosition(line=1, column=10), type=TokenType.RIGHT_CURLY_BRACKET),
                Token(value='elif', source_position=SourcePosition(line=2, column=1), type=TokenType.ELIF),
                Token(value='false', source_position=SourcePosition(line=2, column=6), type=TokenType.BOOL_VALUE_FALSE),
                Token(value='{', source_position=SourcePosition(line=2, column=12), type=TokenType.LEFT_CURLY_BRACKET),
                Token(value='}', source_position=SourcePosition(line=2, column=13), type=TokenType.RIGHT_CURLY_BRACKET),
                Token(value='elif', source_position=SourcePosition(line=3, column=1), type=TokenType.ELIF),
                Token(value='false', source_position=SourcePosition(line=3, column=6), type=TokenType.BOOL_VALUE_FALSE),
                Token(value='{', source_position=SourcePosition(line=3, column=12), type=TokenType.LEFT_CURLY_BRACKET),
                Token(value='}', source_position=SourcePosition(line=3, column=13), type=TokenType.RIGHT_CURLY_BRACKET),
            ],
            IfStatement(
                position=SourcePosition(line=1, column=1),
                condition=BoolConst(position=SourcePosition(line=1, column=4), value=True),
                block=Block(position=SourcePosition(line=1, column=9), statements=[]),
                elif_blocks=[
                    (BoolConst(position=SourcePosition(line=2, column=6), value=False),
                     Block(position=SourcePosition(line=2, column=12), statements=[])),
                    (BoolConst(position=SourcePosition(line=3, column=6), value=False),
                     Block(position=SourcePosition(line=3, column=12), statements=[]))
                ],
                else_block=None
            )
        ),
        # if z jednym elif i jednym else
        (
            [
                Token(value='if', source_position=SourcePosition(line=1, column=1), type=TokenType.IF),
                Token(value='true', source_position=SourcePosition(line=1, column=4), type=TokenType.BOOL_VALUE_TRUE),
                Token(value='{', source_position=SourcePosition(line=1, column=9), type=TokenType.LEFT_CURLY_BRACKET),
                Token(value='}', source_position=SourcePosition(line=1, column=10), type=TokenType.RIGHT_CURLY_BRACKET),
                Token(value='elif', source_position=SourcePosition(line=2, column=1), type=TokenType.ELIF),
                Token(value='false', source_position=SourcePosition(line=2, column=6), type=TokenType.BOOL_VALUE_FALSE),
                Token(value='{', source_position=SourcePosition(line=2, column=12), type=TokenType.LEFT_CURLY_BRACKET),
                Token(value='}', source_position=SourcePosition(line=2, column=13), type=TokenType.RIGHT_CURLY_BRACKET),
                Token(value='else', source_position=SourcePosition(line=3, column=1), type=TokenType.ELSE),
                Token(value='{', source_position=SourcePosition(line=3, column=6), type=TokenType.LEFT_CURLY_BRACKET),
                Token(value='}', source_position=SourcePosition(line=3, column=7), type=TokenType.RIGHT_CURLY_BRACKET),
            ],
            IfStatement(
                position=SourcePosition(line=1, column=1),
                condition=BoolConst(position=SourcePosition(line=1, column=4), value=True),
                block=Block(position=SourcePosition(line=1, column=9), statements=[]),
                elif_blocks=[
                    (BoolConst(position=SourcePosition(line=2, column=6), value=False),
                     Block(position=SourcePosition(line=2, column=12), statements=[]))
                ],
                else_block=Block(position=SourcePosition(line=3, column=6), statements=[])
            )
        ),
        # Brak wyrażenia po if (błąd)
        (
            [
                Token(value='if', source_position=SourcePosition(line=1, column=1), type=TokenType.IF),
                Token(value='if', source_position=SourcePosition(line=1, column=4), type=TokenType.IF),
            ],
            ParserError("Expected an expression after if.", SourcePosition(line=1, column=4))
        ),
        # Brak bloku po if (błąd)
        (
            [
                Token(value='if', source_position=SourcePosition(line=1, column=1), type=TokenType.IF),
                Token(value='true', source_position=SourcePosition(line=1, column=4), type=TokenType.BOOL_VALUE_TRUE),
                Token(value='else', source_position=SourcePosition(line=1, column=9), type=TokenType.ELSE),
            ],
            ParserError("Expected a block in if statement.", SourcePosition(line=1, column=9))
        ),
        # Brak wyrażenia po elif (błąd)
        (
            [
                Token(value='if', source_position=SourcePosition(line=1, column=1), type=TokenType.IF),
                Token(value='true', source_position=SourcePosition(line=1, column=4), type=TokenType.BOOL_VALUE_TRUE),
                Token(value='{', source_position=SourcePosition(line=1, column=9), type=TokenType.LEFT_CURLY_BRACKET),
                Token(value='}', source_position=SourcePosition(line=1, column=10), type=TokenType.RIGHT_CURLY_BRACKET),
                Token(value='elif', source_position=SourcePosition(line=2, column=1), type=TokenType.ELIF),
                Token(value='elif', source_position=SourcePosition(line=2, column=6), type=TokenType.ELIF),
            ],
            ParserError("Expected an expression after elif.", SourcePosition(line=2, column=6))
        ),
        # Brak bloku po elif (błąd)
        (
            [
                Token(value='if', source_position=SourcePosition(line=1, column=1), type=TokenType.IF),
                Token(value='true', source_position=SourcePosition(line=1, column=4), type=TokenType.BOOL_VALUE_TRUE),
                Token(value='{', source_position=SourcePosition(line=1, column=9), type=TokenType.LEFT_CURLY_BRACKET),
                Token(value='}', source_position=SourcePosition(line=1, column=10), type=TokenType.RIGHT_CURLY_BRACKET),
                Token(value='elif', source_position=SourcePosition(line=2, column=1), type=TokenType.ELIF),
                Token(value='false', source_position=SourcePosition(line=2, column=6), type=TokenType.BOOL_VALUE_FALSE),
                Token(value='else', source_position=SourcePosition(line=2, column=12), type=TokenType.ELSE),
            ],
            ParserError("Expected a block after elif statement.", SourcePosition(line=2, column=12))
        ),
        # Brak bloku po else (błąd)
        (
            [
                Token(value='if', source_position=SourcePosition(line=1, column=1), type=TokenType.IF),
                Token(value='true', source_position=SourcePosition(line=1, column=4), type=TokenType.BOOL_VALUE_TRUE),
                Token(value='{', source_position=SourcePosition(line=1, column=9), type=TokenType.LEFT_CURLY_BRACKET),
                Token(value='}', source_position=SourcePosition(line=1, column=10), type=TokenType.RIGHT_CURLY_BRACKET),
                Token(value='else', source_position=SourcePosition(line=2, column=1), type=TokenType.ELSE),
                Token(value='if', source_position=SourcePosition(line=2, column=6), type=TokenType.IF),
            ],
            ParserError("Expected a block after else statement", SourcePosition(line=2, column=6))
        ),
    ])
    def test_parse_conditional(self, tokens, expected_conditional):
        lexer = FakeLexer(tokens)
        parser = Parser(lexer)
        if isinstance(expected_conditional, ParserError):
            with pytest.raises(ParserError) as excinfo:
                parser._parse_conditional()
            assert excinfo.value.message == expected_conditional.message
            assert excinfo.value.position == expected_conditional.position
        else:
            conditional = parser._parse_conditional()
            assert conditional == expected_conditional

    @pytest.mark.parametrize('tokens, expected_loop', [
        # Brak loop
        (
            [
                Token(value='if', source_position=SourcePosition(line=1, column=1), type=TokenType.IF),
            ],
            None
        ),
    ])
    def test_parse_loop(self, tokens, expected_loop):
        lexer = FakeLexer(tokens)
        parser = Parser(lexer)
        if expected_loop is None:
            loop = parser._parse_loop()
            assert loop is None

    @pytest.mark.parametrize('tokens, expected_while_loop', [
        # Poprawna pętla while z wyrażeniem i blokiem
        (
            [
                Token(value='while', source_position=SourcePosition(line=1, column=1), type=TokenType.WHILE),
                Token(value='true', source_position=SourcePosition(line=1, column=7), type=TokenType.BOOL_VALUE_TRUE),
                Token(value='{', source_position=SourcePosition(line=1, column=12), type=TokenType.LEFT_CURLY_BRACKET),
                Token(value='}', source_position=SourcePosition(line=1, column=13), type=TokenType.RIGHT_CURLY_BRACKET),
            ],
            WhileLoopStatement(
                position=SourcePosition(line=1, column=1),
                condition=BoolConst(position=SourcePosition(line=1, column=7), value=True),
                block=Block(position=SourcePosition(line=1, column=12), statements=[])
            )
        ),
        # Brak wyrażenia po while (błąd)
        (
            [
                Token(value='while', source_position=SourcePosition(line=1, column=1), type=TokenType.WHILE),
                Token(value='while', source_position=SourcePosition(line=1, column=7), type=TokenType.WHILE),
            ],
            ParserError("Expected expression after while", SourcePosition(line=1, column=7))
        ),
        # Brak bloku po while (błąd)
        (
            [
                Token(value='while', source_position=SourcePosition(line=1, column=1), type=TokenType.WHILE),
                Token(value='true', source_position=SourcePosition(line=1, column=7), type=TokenType.BOOL_VALUE_TRUE),
                Token(value=';', source_position=SourcePosition(line=1, column=12), type=TokenType.SEMICOLON),
            ],
            ParserError("Expected block in while statement", SourcePosition(line=1, column=12))
        ),
    ])
    def test_parse_while_loop(self, tokens, expected_while_loop):
        lexer = FakeLexer(tokens)
        parser = Parser(lexer)
        if isinstance(expected_while_loop, ParserError):
            with pytest.raises(ParserError) as excinfo:
                parser._parse_while_loop()
            assert excinfo.value.message == expected_while_loop.message
            assert excinfo.value.position == expected_while_loop.position
        else:
            while_loop = parser._parse_while_loop()
            assert while_loop == expected_while_loop

    @pytest.mark.parametrize('tokens, expected_for_loop', [
        # Poprawna pętla for z wyrażeniem i blokiem
        (
            [
                Token(value='for', source_position=SourcePosition(line=1, column=1), type=TokenType.FOR),
                Token(value='i', source_position=SourcePosition(line=1, column=5), type=TokenType.IDENTIFIER),
                Token(value='in', source_position=SourcePosition(line=1, column=7), type=TokenType.IN),
                Token(value='my_dict', source_position=SourcePosition(line=1, column=10), type=TokenType.IDENTIFIER),
                Token(value='{', source_position=SourcePosition(line=1, column=18), type=TokenType.LEFT_CURLY_BRACKET),
                Token(value='}', source_position=SourcePosition(line=1, column=19), type=TokenType.RIGHT_CURLY_BRACKET),
            ],
            ForLoopStatement(
                position=SourcePosition(line=1, column=1),
                loop_identifier='i',
                expression=ObjectAccess(
                    position=SourcePosition(line=1, column=10),
                    objects=[
                        IdentifierExpression(
                            position=SourcePosition(line=1, column=10),
                            name='my_dict'
                        )
                    ]
                ),
                block=Block(position=SourcePosition(line=1, column=18), statements=[])
            )
        ),
        # Brak in (błąd)
        (
            [
                Token(value='for', source_position=SourcePosition(line=1, column=1), type=TokenType.FOR),
                Token(value='i', source_position=SourcePosition(line=1, column=5), type=TokenType.IDENTIFIER),
                Token(value='my_dict', source_position=SourcePosition(line=1, column=7), type=TokenType.IDENTIFIER),
            ],
            ParserError("Expected IN, got IDENTIFIER", SourcePosition(line=1, column=7))
        ),
        # Brak identyfikatora po for (błąd)
        (
            [
                Token(value='for', source_position=SourcePosition(line=1, column=1), type=TokenType.FOR),
                Token(value='in', source_position=SourcePosition(line=1, column=5), type=TokenType.IN),
            ],
            ParserError("Expected IDENTIFIER, got IN while building for statement.", SourcePosition(line=1, column=5))
        ),
        # Brak wyrażenia po in (błąd)
        (
            [
                Token(value='for', source_position=SourcePosition(line=1, column=1), type=TokenType.FOR),
                Token(value='i', source_position=SourcePosition(line=1, column=5), type=TokenType.IDENTIFIER),
                Token(value='in', source_position=SourcePosition(line=1, column=7), type=TokenType.IN),
                Token(value='in', source_position=SourcePosition(line=1, column=10), type=TokenType.IN),
            ],
            ParserError("Expected expression after \"in\".", SourcePosition(line=1, column=10))
        ),
        # Brak bloku po for (błąd)
        (
            [
                Token(value='for', source_position=SourcePosition(line=1, column=1), type=TokenType.FOR),
                Token(value='i', source_position=SourcePosition(line=1, column=5), type=TokenType.IDENTIFIER),
                Token(value='in', source_position=SourcePosition(line=1, column=7), type=TokenType.IN),
                Token(value='my_dict', source_position=SourcePosition(line=1, column=10), type=TokenType.IDENTIFIER),
                Token(value=';', source_position=SourcePosition(line=1, column=18), type=TokenType.SEMICOLON),
            ],
            ParserError("Expected block in for statement", SourcePosition(line=1, column=18))
        ),
    ])
    def test_parse_for_loop(self, tokens, expected_for_loop):
        lexer = FakeLexer(tokens)
        parser = Parser(lexer)
        if isinstance(expected_for_loop, ParserError):
            with pytest.raises(ParserError) as excinfo:
                parser._parse_for_loop()
            assert excinfo.value.message == expected_for_loop.message
            assert excinfo.value.position == expected_for_loop.position
        else:
            for_loop = parser._parse_for_loop()
            assert for_loop == expected_for_loop

    @pytest.mark.parametrize('tokens, expected_return_statement', [
        # Poprawne return z wyrażeniem
        (
            [
                Token(value='return', source_position=SourcePosition(line=1, column=1), type=TokenType.RETURN),
                Token(value=42, source_position=SourcePosition(line=1, column=8), type=TokenType.INT_CONST),
                Token(value=';', source_position=SourcePosition(line=1, column=10), type=TokenType.SEMICOLON),
            ],
            ReturnStatement(
                position=SourcePosition(line=1, column=1),
                expression=IntConst(position=SourcePosition(line=1, column=8), value=42)
            )
        ),
        # Poprawne return bez wyrażenia
        (
            [
                Token(value='return', source_position=SourcePosition(line=1, column=1), type=TokenType.RETURN),
                Token(value=';', source_position=SourcePosition(line=1, column=8), type=TokenType.SEMICOLON),
            ],
            ReturnStatement(
                position=SourcePosition(line=1, column=1),
                expression=None
            )
        ),
        # Brak średnika po return (błąd)
        (
            [
                Token(value='return', source_position=SourcePosition(line=1, column=1), type=TokenType.RETURN),
                Token(value=42, source_position=SourcePosition(line=1, column=8), type=TokenType.INT_CONST),
                Token(value='', source_position=SourcePosition(line=1, column=11), type=TokenType.END_OF_FILE),
            ],
            ParserError("Expected SEMICOLON, got END_OF_FILE", SourcePosition(line=1, column=11))
        ),
    ])
    def test_parse_return_statement(self, tokens, expected_return_statement):
        lexer = FakeLexer(tokens)
        parser = Parser(lexer)
        if isinstance(expected_return_statement, ParserError):
            with pytest.raises(ParserError) as excinfo:
                parser._parse_return_statement()
            assert excinfo.value.message == expected_return_statement.message
            assert excinfo.value.position == expected_return_statement.position
        else:
            return_statement = parser._parse_return_statement()
            assert return_statement == expected_return_statement

    @pytest.mark.parametrize('tokens, expected_currency_transfer', [
        # Poprawny transfer waluty z dwoma wyrażeniami
        (
            [
                Token(value='from', source_position=SourcePosition(line=1, column=1), type=TokenType.FROM),
                Token(value='account1', source_position=SourcePosition(line=1, column=6), type=TokenType.IDENTIFIER),
                Token(value='->', source_position=SourcePosition(line=1, column=14), type=TokenType.CUR_TRANSFER),
                Token(value='amount', source_position=SourcePosition(line=1, column=17), type=TokenType.IDENTIFIER),
                Token(value=';', source_position=SourcePosition(line=1, column=25), type=TokenType.SEMICOLON),
            ],
            CurrencyTransfer(
                position=SourcePosition(line=1, column=1),
                expressions=[
                    ObjectAccess(
                        position=SourcePosition(line=1, column=6),
                        objects=[IdentifierExpression(position=SourcePosition(line=1, column=6), name='account1')]
                    ),
                    ObjectAccess(
                        position=SourcePosition(line=1, column=17),
                        objects=[IdentifierExpression(position=SourcePosition(line=1, column=17), name='amount')]
                    )
                ]
            )
        ),
        # Poprawny transfer waluty z trzema wyrażeniami
        (
            [
                Token(value='from', source_position=SourcePosition(line=1, column=1), type=TokenType.FROM),
                Token(value='account1', source_position=SourcePosition(line=1, column=6), type=TokenType.IDENTIFIER),
                Token(value='->', source_position=SourcePosition(line=1, column=14), type=TokenType.CUR_TRANSFER),
                Token(value='amount', source_position=SourcePosition(line=1, column=17), type=TokenType.IDENTIFIER),
                Token(value='->', source_position=SourcePosition(line=1, column=24), type=TokenType.CUR_TRANSFER),
                Token(value='account2', source_position=SourcePosition(line=1, column=27), type=TokenType.IDENTIFIER),
                Token(value=';', source_position=SourcePosition(line=1, column=35), type=TokenType.SEMICOLON),
            ],
            CurrencyTransfer(
                position=SourcePosition(line=1, column=1),
                expressions=[
                    ObjectAccess(
                        position=SourcePosition(line=1, column=6),
                        objects=[IdentifierExpression(position=SourcePosition(line=1, column=6), name='account1')]
                    ),
                    ObjectAccess(
                        position=SourcePosition(line=1, column=17),
                        objects=[IdentifierExpression(position=SourcePosition(line=1, column=17), name='amount')]
                    ),
                    ObjectAccess(
                        position=SourcePosition(line=1, column=27),
                        objects=[IdentifierExpression(position=SourcePosition(line=1, column=27), name='account2')]
                    )
                ]
            )
        ),
        # Brak wyrażenia po 'from' (błąd)
        (
            [
                Token(value='from', source_position=SourcePosition(line=1, column=1), type=TokenType.FROM),
                Token(value='->', source_position=SourcePosition(line=1, column=6), type=TokenType.CUR_TRANSFER),
                Token(value='account2', source_position=SourcePosition(line=1, column=9), type=TokenType.IDENTIFIER),
                Token(value=';', source_position=SourcePosition(line=1, column=17), type=TokenType.SEMICOLON),
            ],
            ParserError("Expected an expression after from keyword", SourcePosition(line=1, column=6))
        ),
        # Brak wyrażenia po pierwszym '->' (błąd)
        (
            [
                Token(value='from', source_position=SourcePosition(line=1, column=1), type=TokenType.FROM),
                Token(value='account1', source_position=SourcePosition(line=1, column=6), type=TokenType.IDENTIFIER),
                Token(value='->', source_position=SourcePosition(line=1, column=14), type=TokenType.CUR_TRANSFER),
                Token(value=';', source_position=SourcePosition(line=1, column=17), type=TokenType.SEMICOLON),
            ],
            ParserError("Expected an expression after ->", SourcePosition(line=1, column=17))
        ),
        # Brak pierwszego '->' (błąd)
        (
            [
                Token(value='from', source_position=SourcePosition(line=1, column=1), type=TokenType.FROM),
                Token(value='account1', source_position=SourcePosition(line=1, column=6), type=TokenType.IDENTIFIER),
                Token(value='account2', source_position=SourcePosition(line=1, column=14), type=TokenType.IDENTIFIER),
                Token(value=';', source_position=SourcePosition(line=1, column=17), type=TokenType.SEMICOLON),
            ],
            ParserError("Expected CUR_TRANSFER, got IDENTIFIER", SourcePosition(line=1, column=14))
        ),
        # Brak wyrażenia po drugim '->' (błąd)
        (
            [
                Token(value='from', source_position=SourcePosition(line=1, column=1), type=TokenType.FROM),
                Token(value='account1', source_position=SourcePosition(line=1, column=6), type=TokenType.IDENTIFIER),
                Token(value='->', source_position=SourcePosition(line=1, column=14), type=TokenType.CUR_TRANSFER),
                Token(value='amount', source_position=SourcePosition(line=1, column=17), type=TokenType.IDENTIFIER),
                Token(value='->', source_position=SourcePosition(line=1, column=24), type=TokenType.CUR_TRANSFER),
                Token(value=';', source_position=SourcePosition(line=1, column=27), type=TokenType.SEMICOLON),
            ],
            ParserError("Expected an expression after ->", SourcePosition(line=1, column=27))
        ),
    ])
    def test_parse_currency_transfer(self, tokens, expected_currency_transfer):
        lexer = FakeLexer(tokens)
        parser = Parser(lexer)
        if isinstance(expected_currency_transfer, ParserError):
            with pytest.raises(ParserError) as excinfo:
                parser._parse_currency_transfer()
            assert excinfo.value.message == expected_currency_transfer.message
            assert excinfo.value.position == expected_currency_transfer.position
        else:
            currency_transfer = parser._parse_currency_transfer()
            assert currency_transfer == expected_currency_transfer

    @pytest.mark.parametrize('tokens, expected_expression', [
        # Poprawne wyrażenie z jednym conjunction
        (
            [
                Token(value='true', source_position=SourcePosition(line=1, column=1), type=TokenType.BOOL_VALUE_TRUE),
            ],
            BoolConst(position=SourcePosition(line=1, column=1), value=True)
        ),
        # Poprawne wyrażenie z dwoma conjunction połączonymi operatorem OR
        (
            [
                Token(value='true', source_position=SourcePosition(line=1, column=1), type=TokenType.BOOL_VALUE_TRUE),
                Token(value='||', source_position=SourcePosition(line=1, column=6), type=TokenType.OR),
                Token(value='false', source_position=SourcePosition(line=1, column=9), type=TokenType.BOOL_VALUE_FALSE),
            ],
            OrExpression(
                position=SourcePosition(line=1, column=6),
                left=BoolConst(position=SourcePosition(line=1, column=1), value=True),
                right=BoolConst(position=SourcePosition(line=1, column=9), value=False)
            )
        ),
        # Poprawne wyrażenie z trzema conjunction połączonymi operatorem OR
        (
            [
                Token(value='true', source_position=SourcePosition(line=1, column=1), type=TokenType.BOOL_VALUE_TRUE),
                Token(value='||', source_position=SourcePosition(line=1, column=6), type=TokenType.OR),
                Token(value='false', source_position=SourcePosition(line=1, column=9), type=TokenType.BOOL_VALUE_FALSE),
                Token(value='||', source_position=SourcePosition(line=1, column=15), type=TokenType.OR),
                Token(value='false', source_position=SourcePosition(line=1, column=18), type=TokenType.BOOL_VALUE_FALSE)
            ],
            OrExpression(
                position=SourcePosition(line=1, column=15),
                left=OrExpression(
                    position=SourcePosition(line=1, column=6),
                    left=BoolConst(position=SourcePosition(line=1, column=1), value=True),
                    right=BoolConst(position=SourcePosition(line=1, column=9), value=False)
                ),
                right=BoolConst(position=SourcePosition(line=1, column=18), value=False)
            )
        ),
        # Brak drugiego conjuction po OR (błąd)
        (
            [
                Token(value='true', source_position=SourcePosition(line=1, column=1), type=TokenType.BOOL_VALUE_TRUE),
                Token(value='||', source_position=SourcePosition(line=1, column=6), type=TokenType.OR),
            ],
            ParserError("Missing expression after ||.", SourcePosition(line=1, column=6))
        ),
    ])
    def test_parse_expression(self, tokens, expected_expression):
        lexer = FakeLexer(tokens)
        parser = Parser(lexer)
        if isinstance(expected_expression, ParserError):
            with pytest.raises(ParserError) as excinfo:
                parser._parse_expression()
            assert excinfo.value.message == expected_expression.message
            assert excinfo.value.position == expected_expression.position
        else:
            expression = parser._parse_expression()
            assert expression == expected_expression

    @pytest.mark.parametrize('tokens, expected_conjunction', [
        # Poprawny koniunkcja z jedną negacją
        (
            [
                Token(value='true', source_position=SourcePosition(line=1, column=1), type=TokenType.BOOL_VALUE_TRUE),
            ],
            BoolConst(position=SourcePosition(line=1, column=1), value=True)
        ),
        # Poprawna koniunkcja z dwiema negacjami połączonymi operatorem AND
        (
            [
                Token(value='true', source_position=SourcePosition(line=1, column=1), type=TokenType.BOOL_VALUE_TRUE),
                Token(value='&&', source_position=SourcePosition(line=1, column=6), type=TokenType.AND),
                Token(value='false', source_position=SourcePosition(line=1, column=9), type=TokenType.BOOL_VALUE_FALSE),
            ],
            AndExpression(
                position=SourcePosition(line=1, column=6),
                left=BoolConst(position=SourcePosition(line=1, column=1), value=True),
                right=BoolConst(position=SourcePosition(line=1, column=9), value=False)
            )
        ),
        # Poprawna koniunkcja z trzema negacjami połączonymi operatorem AND
        (
            [
                Token(value='true', source_position=SourcePosition(line=1, column=1), type=TokenType.BOOL_VALUE_TRUE),
                Token(value='&&', source_position=SourcePosition(line=1, column=6), type=TokenType.AND),
                Token(value='false', source_position=SourcePosition(line=1, column=9), type=TokenType.BOOL_VALUE_FALSE),
                Token(value='&&', source_position=SourcePosition(line=1, column=15), type=TokenType.AND),
                Token(value='false', source_position=SourcePosition(line=1, column=18), type=TokenType.BOOL_VALUE_FALSE)
            ],
            AndExpression(
                position=SourcePosition(line=1, column=15),
                left=AndExpression(
                    position=SourcePosition(line=1, column=6),
                    left=BoolConst(position=SourcePosition(line=1, column=1), value=True),
                    right=BoolConst(position=SourcePosition(line=1, column=9), value=False)
                ),
                right=BoolConst(position=SourcePosition(line=1, column=18), value=False)
            )
        ),
        # Brak drugiej negacji po AND (błąd)
        (
            [
                Token(value='true', source_position=SourcePosition(line=1, column=1), type=TokenType.BOOL_VALUE_TRUE),
                Token(value='&&', source_position=SourcePosition(line=1, column=6), type=TokenType.AND),
            ],
            ParserError("Missing expression after &&.", SourcePosition(line=1, column=6))
        ),
    ])
    def test_parse_conjunction(self, tokens, expected_conjunction):
        lexer = FakeLexer(tokens)
        parser = Parser(lexer)
        if isinstance(expected_conjunction, ParserError):
            with pytest.raises(ParserError) as excinfo:
                parser._parse_conjunction()
            assert excinfo.value.message == expected_conjunction.message
            assert excinfo.value.position == expected_conjunction.position
        else:
            conjunction = parser._parse_conjunction()
            assert conjunction == expected_conjunction

    @pytest.mark.parametrize('tokens, expected_negation', [
        # Poprawna negacja
        (
            [
                Token(value='!', source_position=SourcePosition(line=1, column=1), type=TokenType.NOT),
                Token(value='true', source_position=SourcePosition(line=1, column=2), type=TokenType.BOOL_VALUE_TRUE),
            ],
            NegatedExpression(
                position=SourcePosition(line=1, column=1),
                left="!",
                right=BoolConst(position=SourcePosition(line=1, column=2), value=True)
            )
        ),
        # Poprawna negacja z brakiem wyrażenia (błąd)
        (
            [
                Token(value='!', source_position=SourcePosition(line=1, column=1), type=TokenType.NOT),
                Token(value='', source_position=SourcePosition(line=1, column=3), type=TokenType.END_OF_FILE),
            ],
            ParserError("Expected expression after \"!\"", SourcePosition(line=1, column=1))
        ),
        # Brak negacji
        (
            [
                Token(value='true', source_position=SourcePosition(line=1, column=1), type=TokenType.BOOL_VALUE_TRUE),
            ],
            BoolConst(position=SourcePosition(line=1, column=1), value=True)
        ),
    ])
    def test_parse_negation(self, tokens, expected_negation):
        lexer = FakeLexer(tokens)
        parser = Parser(lexer)
        if isinstance(expected_negation, ParserError):
            with pytest.raises(ParserError) as excinfo:
                parser._parse_negation()
            assert excinfo.value.message == expected_negation.message
            assert excinfo.value.position == expected_negation.position
        else:
            negation = parser._parse_negation()
            assert negation == expected_negation

    @pytest.mark.parametrize('tokens, expected_relation_term', [
        # Poprawny relation_term z jednym additive_term
        (
            [
                Token(value=1, source_position=SourcePosition(line=1, column=1), type=TokenType.INT_CONST),
            ],
            IntConst(position=SourcePosition(line=1, column=1), value=1)
        ),
        # Poprawny relation_term z dwoma additive_term połączonymi operatorem równości
        (
            [
                Token(value=1, source_position=SourcePosition(line=1, column=1), type=TokenType.INT_CONST),
                Token(value='==', source_position=SourcePosition(line=1, column=2), type=TokenType.EQUAL),
                Token(value=2, source_position=SourcePosition(line=1, column=4), type=TokenType.INT_CONST),
            ],
            EqualRelation(
                position=SourcePosition(line=1, column=2),
                left=IntConst(position=SourcePosition(line=1, column=1), value=1),
                right=IntConst(position=SourcePosition(line=1, column=4), value=2)
            )
        ),
        # Brak drugiego additive_term po operatorze relacji (błąd)
        (
            [
                Token(value=1, source_position=SourcePosition(line=1, column=1), type=TokenType.INT_CONST),
                Token(value='>', source_position=SourcePosition(line=1, column=2), type=TokenType.GREATER),
            ],
            ParserError("Missing expression after GREATER.", SourcePosition(line=1, column=2))
        ),
    ])
    def test_parse_relation_term(self, tokens, expected_relation_term):
        lexer = FakeLexer(tokens)
        parser = Parser(lexer)
        if isinstance(expected_relation_term, ParserError):
            with pytest.raises(ParserError) as excinfo:
                parser._parse_relation_term()
            assert excinfo.value.message == expected_relation_term.message
            assert excinfo.value.position == expected_relation_term.position
        else:
            relation_term = parser._parse_relation_term()
            assert relation_term == expected_relation_term

    @pytest.mark.parametrize('tokens, expected_additive_term', [
        # Poprawny additive_term z jednym multiplicative_term
        (
            [
                Token(value=2, source_position=SourcePosition(line=1, column=1), type=TokenType.INT_CONST),
            ],
            IntConst(position=SourcePosition(line=1, column=1), value=2)
        ),
        # Poprawny additive_term z dwoma multiplicative_term połączonymi operatorem dodawania
        (
            [
                Token(value=2, source_position=SourcePosition(line=1, column=1), type=TokenType.INT_CONST),
                Token(value='+', source_position=SourcePosition(line=1, column=2), type=TokenType.PLUS),
                Token(value=3, source_position=SourcePosition(line=1, column=3), type=TokenType.INT_CONST),
            ],
            AddExpression(
                position=SourcePosition(line=1, column=2),
                left=IntConst(position=SourcePosition(line=1, column=1), value=2),
                right=IntConst(position=SourcePosition(line=1, column=3), value=3)
            )
        ),
        # Poprawny additive_term z trzema multiplicative_term połączonymi operatorem dodawania
        (
            [
                Token(value=2, source_position=SourcePosition(line=1, column=1), type=TokenType.INT_CONST),
                Token(value='+', source_position=SourcePosition(line=1, column=2), type=TokenType.PLUS),
                Token(value=3, source_position=SourcePosition(line=1, column=3), type=TokenType.INT_CONST),
                Token(value='+', source_position=SourcePosition(line=1, column=4), type=TokenType.PLUS),
                Token(value=4, source_position=SourcePosition(line=1, column=5), type=TokenType.INT_CONST),
            ],
            AddExpression(
                position=SourcePosition(line=1, column=4),
                left=AddExpression(
                    position=SourcePosition(line=1, column=2),
                    left=IntConst(position=SourcePosition(line=1, column=1), value=2),
                    right=IntConst(position=SourcePosition(line=1, column=3), value=3)
                ),
                right=IntConst(position=SourcePosition(line=1, column=5), value=4)
            )
        ),
        # Poprawny additive_term z dwoma multiplicative_term połączonymi operatorem odejmowania
        (
            [
                Token(value=2, source_position=SourcePosition(line=1, column=1), type=TokenType.INT_CONST),
                Token(value='-', source_position=SourcePosition(line=1, column=2), type=TokenType.MINUS),
                Token(value=3, source_position=SourcePosition(line=1, column=3), type=TokenType.INT_CONST),
            ],
            SubExpression(
                position=SourcePosition(line=1, column=2),
                left=IntConst(position=SourcePosition(line=1, column=1), value=2),
                right=IntConst(position=SourcePosition(line=1, column=3), value=3)
            )
        ),
        # Brak drugiego multiplicative_term po operatorze dodawania (błąd)
        (
            [
                Token(value='2', source_position=SourcePosition(line=1, column=1), type=TokenType.INT_CONST),
                Token(value='+', source_position=SourcePosition(line=1, column=2), type=TokenType.PLUS),
                Token(value='', source_position=SourcePosition(line=1, column=3), type=TokenType.END_OF_FILE),
            ],
            ParserError("Missing expression after PLUS.", SourcePosition(line=1, column=2))
        ),
    ])
    def test_parse_additive_term(self, tokens, expected_additive_term):
        lexer = FakeLexer(tokens)
        parser = Parser(lexer)
        if isinstance(expected_additive_term, ParserError):
            with pytest.raises(ParserError) as excinfo:
                parser._parse_additive_term()
            assert excinfo.value.message == expected_additive_term.message
            assert excinfo.value.position == expected_additive_term.position
        else:
            additive_term = parser._parse_additive_term()
            assert additive_term == expected_additive_term

    @pytest.mark.parametrize('tokens, expected_multiplicative_term', [
        # Poprawny multiplicative_term z jednym unary_application
        (
            [
                Token(value=3, source_position=SourcePosition(line=1, column=1), type=TokenType.INT_CONST),
            ],
            IntConst(position=SourcePosition(line=1, column=1), value=3)
        ),
        # Poprawny multiplicative_term z dwoma unary_application połączonymi operatorem mnożenia
        (
            [
                Token(value=3, source_position=SourcePosition(line=1, column=1), type=TokenType.INT_CONST),
                Token(value='*', source_position=SourcePosition(line=1, column=2), type=TokenType.MUL),
                Token(value=2, source_position=SourcePosition(line=1, column=3), type=TokenType.INT_CONST),
            ],
            MulExpression(
                position=SourcePosition(line=1, column=2),
                left=IntConst(position=SourcePosition(line=1, column=1), value=3),
                right=IntConst(position=SourcePosition(line=1, column=3), value=2)
            )
        ),
        # Poprawny multipicative_term z trzema unary_application połączonymi operatorem mnożenia
        (
            [
                Token(value=3, source_position=SourcePosition(line=1, column=1), type=TokenType.INT_CONST),
                Token(value='*', source_position=SourcePosition(line=1, column=2), type=TokenType.MUL),
                Token(value=2, source_position=SourcePosition(line=1, column=3), type=TokenType.INT_CONST),
                Token(value='*', source_position=SourcePosition(line=1, column=4), type=TokenType.MUL),
                Token(value=1, source_position=SourcePosition(line=1, column=5), type=TokenType.INT_CONST),
            ],
            MulExpression(
                position=SourcePosition(line=1, column=4),
                left=MulExpression(
                    position=SourcePosition(line=1, column=2),
                    left=IntConst(position=SourcePosition(line=1, column=1), value=3),
                    right=IntConst(position=SourcePosition(line=1, column=3), value=2)
                ),
                right=IntConst(position=SourcePosition(line=1, column=5), value=1)
            )
        ),
        # Poprawny multiplicative_term z dwoma unary_application połączonymi operatorem dzielenia
        (
            [
                Token(value=3, source_position=SourcePosition(line=1, column=1), type=TokenType.INT_CONST),
                Token(value='/', source_position=SourcePosition(line=1, column=2), type=TokenType.DIV),
                Token(value=2, source_position=SourcePosition(line=1, column=3), type=TokenType.INT_CONST),
            ],
            DivExpression(
                position=SourcePosition(line=1, column=2),
                left=IntConst(position=SourcePosition(line=1, column=1), value=3),
                right=IntConst(position=SourcePosition(line=1, column=3), value=2)
            )
        ),
        # Brak drugiego unary_application po operatorze mnożenia (błąd)
        (
            [
                Token(value=3, source_position=SourcePosition(line=1, column=1), type=TokenType.INT_CONST),
                Token(value='*', source_position=SourcePosition(line=1, column=2), type=TokenType.MUL),
            ],
            ParserError("Missing expression after MUL.", SourcePosition(line=1, column=2))
        ),
    ])
    def test_parse_multiplicative_term(self, tokens, expected_multiplicative_term):
        lexer = FakeLexer(tokens)
        parser = Parser(lexer)
        if isinstance(expected_multiplicative_term, ParserError):
            with pytest.raises(ParserError) as excinfo:
                parser._parse_multiplicative_term()
            assert excinfo.value.message == expected_multiplicative_term.message
            assert excinfo.value.position == expected_multiplicative_term.position
        else:
            multiplicative_term = parser._parse_multiplicative_term()
            assert multiplicative_term == expected_multiplicative_term

    @pytest.mark.parametrize('tokens, expected_unary_application', [
        # Poprawne unary_application z term jako IntConst
        (
            [
                Token(value=3, source_position=SourcePosition(line=1, column=1), type=TokenType.INT_CONST),
            ],
            IntConst(position=SourcePosition(line=1, column=1), value=3)
        ),
        # Poprawne unary_application z term jako FloatConst
        (
            [
                Token(value='-', source_position=SourcePosition(line=1, column=1), type=TokenType.MINUS),
                Token(value=2.5, source_position=SourcePosition(line=1, column=2), type=TokenType.FLOAT_CONST),
            ],
            NegatedExpression(
                position=SourcePosition(line=1, column=1),
                left="-",
                right=FloatConst(position=SourcePosition(line=1, column=2), value=2.5)
            )
        ),
        # Brak term po znaku minus (błąd)
        (
            [
                Token(value='-', source_position=SourcePosition(line=1, column=1), type=TokenType.MINUS),
                Token(value='', source_position=SourcePosition(line=1, column=2), type=TokenType.END_OF_FILE),
            ],
            ParserError("Expected expression after \"-\"", SourcePosition(line=1, column=1))
        ),
    ])
    def test_parse_unary_application(self, tokens, expected_unary_application):
        lexer = FakeLexer(tokens)
        parser = Parser(lexer)
        if isinstance(expected_unary_application, ParserError):
            with pytest.raises(ParserError) as excinfo:
                parser._parse_unary_application()
            assert excinfo.value.message == expected_unary_application.message
            assert excinfo.value.position == expected_unary_application.position
        else:
            unary_application = parser._parse_unary_application()
            assert unary_application == expected_unary_application

    @pytest.mark.parametrize('tokens, expected_term', [
        (
            [
                Token(value=';', source_position=SourcePosition(line=1, column=1), type=TokenType.SEMICOLON),
                Token(value='', source_position=SourcePosition(line=1, column=2), type=TokenType.END_OF_FILE),
            ],
            None
        ),
    ])
    def test_parse_term(self, tokens, expected_term):
        lexer = FakeLexer(tokens)
        parser = Parser(lexer)
        if expected_term is None:
            term = parser._parse_term()
            assert term is None

    @pytest.mark.parametrize('tokens, expected_literal', [
        (
            [
                Token(value=';', source_position=SourcePosition(line=1, column=1), type=TokenType.SEMICOLON),
                Token(value='', source_position=SourcePosition(line=1, column=2), type=TokenType.END_OF_FILE),
            ],
            None
        ),
    ])
    def test_parse_literal(self, tokens, expected_literal):
        lexer = FakeLexer(tokens)
        parser = Parser(lexer)
        if expected_literal is None:
            literal = parser._parse_literal()
            assert literal is None

    @pytest.mark.parametrize('tokens, expected_result', [
        # Poprawne parsowanie int
        (
            [
                Token(value=123, source_position=SourcePosition(line=1, column=1), type=TokenType.INT_CONST)
            ],
            IntConst(position=SourcePosition(line=1, column=1), value=123)
        ),
        # Poprawne parsowanie int z currency
        (
            [
                Token(value=123, source_position=SourcePosition(line=1, column=1), type=TokenType.INT_CONST),
                Token(value='USD', source_position=SourcePosition(line=1, column=4), type=TokenType.CURTYPE_CONST)
            ],
            CurConst(position=SourcePosition(line=1, column=1), value=123, type='USD')
        ),
        # Brak int (błąd)
        (
            [
                Token(value=123.45, source_position=SourcePosition(line=1, column=1), type=TokenType.FLOAT_CONST)
            ],
            None
        ),
    ])
    def test_parse_int_or_cur(self, tokens, expected_result):
        lexer = FakeLexer(tokens)
        parser = Parser(lexer)
        result = parser._parse_int_or_cur()
        assert result == expected_result

    @pytest.mark.parametrize('tokens, expected_result', [
        # Poprawne parsowanie float
        (
            [
                Token(value=123.45, source_position=SourcePosition(line=1, column=1), type=TokenType.FLOAT_CONST)
            ],
            FloatConst(position=SourcePosition(line=1, column=1), value=123.45)
        ),
        # Poprawne parsowanie float z currency
        (
            [
                Token(value=123.45, source_position=SourcePosition(line=1, column=1), type=TokenType.FLOAT_CONST),
                Token(value='USD', source_position=SourcePosition(line=1, column=7), type=TokenType.CURTYPE_CONST)
            ],
            CurConst(position=SourcePosition(line=1, column=1), value=123.45, type='USD')
        ),
        # Brak float (błąd)
        (
            [
                Token(value=123, source_position=SourcePosition(line=1, column=1), type=TokenType.INT_CONST)
            ],
            None
        ),
    ])
    def test_parse_float_or_cur(self, tokens, expected_result):
        lexer = FakeLexer(tokens)
        parser = Parser(lexer)
        result = parser._parse_float_or_cur()
        assert result == expected_result

    @pytest.mark.parametrize('tokens, position, number, expected_result', [
        # Poprawne parsowanie cur
        (
            [
                Token(value='USD', source_position=SourcePosition(line=1, column=4), type=TokenType.CURTYPE_CONST)
            ],
            SourcePosition(line=1, column=1),
            123,
            CurConst(position=SourcePosition(line=1, column=1), value=123, type='USD')
        ),
        # Brak cur (błąd)
        (
            [
                Token(value=123, source_position=SourcePosition(line=1, column=1), type=TokenType.INT_CONST)
            ],
            SourcePosition(line=1, column=1),
            123,
            None
        ),
    ])
    def test_parse_cur(self, tokens, position, number, expected_result):
        lexer = FakeLexer(tokens)
        parser = Parser(lexer)
        result = parser._parse_cur(position, number)
        assert result == expected_result

    @pytest.mark.parametrize('tokens, expected_result', [
        # Poprawne parsowanie stringa
        (
            [
                Token(value='hello', source_position=SourcePosition(line=1, column=1), type=TokenType.STR_CONST)
            ],
            StrConst(position=SourcePosition(line=1, column=1), value='hello')
        ),
        # Brak stringa (błąd)
        (
            [
                Token(value=123, source_position=SourcePosition(line=1, column=1), type=TokenType.INT_CONST)
            ],
            None
        ),
    ])
    def test_parse_str(self, tokens, expected_result):
        lexer = FakeLexer(tokens)
        parser = Parser(lexer)
        result = parser._parse_str()
        assert result == expected_result

    @pytest.mark.parametrize('tokens, expected_result', [
        # Poprawne parsowanie wartości true
        (
            [
                Token(value='true', source_position=SourcePosition(line=1, column=1), type=TokenType.BOOL_VALUE_TRUE)
            ],
            BoolConst(position=SourcePosition(line=1, column=1), value=True)
        ),
        # Poprawne parsowanie wartości false
        (
            [
                Token(value='false', source_position=SourcePosition(line=1, column=1), type=TokenType.BOOL_VALUE_FALSE)
            ],
            BoolConst(position=SourcePosition(line=1, column=1), value=False)
        ),
        # Błędny token (nie-boolean)
        (
            [
                Token(value=123, source_position=SourcePosition(line=1, column=1), type=TokenType.INT_CONST)
            ],
            None
        ),
    ])
    def test_parse_bool(self, tokens, expected_result):
        lexer = FakeLexer(tokens)
        parser = Parser(lexer)
        result = parser._parse_bool()
        assert result == expected_result

    @pytest.mark.parametrize('tokens, expected_result', [
        # Poprawne parsowanie wartości typu waluty
        (
            [
                Token(value='USD', source_position=SourcePosition(line=1, column=1), type=TokenType.CURTYPE_CONST)
            ],
            CurtypeConst(position=SourcePosition(line=1, column=1), value='USD')
        ),
        (
            [
                Token(value='EUR', source_position=SourcePosition(line=2, column=5), type=TokenType.CURTYPE_CONST)
            ],
            CurtypeConst(position=SourcePosition(line=2, column=5), value='EUR')
        ),
        # Błędny token (nie-waluta)
        (
            [
                Token(value=123, source_position=SourcePosition(line=1, column=1), type=TokenType.INT_CONST)
            ],
            None
        ),
    ])
    def test_parse_curtype(self, tokens, expected_result):
        lexer = FakeLexer(tokens)
        parser = Parser(lexer)
        result = parser._parse_curtype()
        assert result == expected_result

    @pytest.mark.parametrize('tokens, expected_result', [
        # Poprawne parsowanie słownika z jedną parą
        (
            [
                Token(value='{', source_position=SourcePosition(line=1, column=1), type=TokenType.LEFT_CURLY_BRACKET),
                Token(value='key', source_position=SourcePosition(line=1, column=2), type=TokenType.STR_CONST),
                Token(value=':', source_position=SourcePosition(line=1, column=7), type=TokenType.COLON),
                Token(value=100, source_position=SourcePosition(line=1, column=8), type=TokenType.INT_CONST),
                Token(value='USD', source_position=SourcePosition(line=1, column=12), type=TokenType.CURTYPE_CONST),
                Token(value='}', source_position=SourcePosition(line=1, column=15), type=TokenType.RIGHT_CURLY_BRACKET),
            ],
            DictConst(
                position=SourcePosition(line=1, column=1),
                pairs=[
                    Pair(
                        position=SourcePosition(line=1, column=2),
                        name='key',
                        expression=CurConst(position=SourcePosition(line=1, column=8), value=100, type='USD')
                    )
                ]
            )
        ),
        # Poprawne parsowanie słownika z dwoma parami
        (
            [
                Token(value='{', source_position=SourcePosition(line=1, column=1), type=TokenType.LEFT_CURLY_BRACKET),
                Token(value='key', source_position=SourcePosition(line=1, column=2), type=TokenType.STR_CONST),
                Token(value=':', source_position=SourcePosition(line=1, column=7), type=TokenType.COLON),
                Token(value=100, source_position=SourcePosition(line=1, column=8), type=TokenType.INT_CONST),
                Token(value='USD', source_position=SourcePosition(line=1, column=12), type=TokenType.CURTYPE_CONST),
                Token(value=',', source_position=SourcePosition(line=1, column=15), type=TokenType.COMMA),
                Token(value='key2', source_position=SourcePosition(line=2, column=2), type=TokenType.STR_CONST),
                Token(value=':', source_position=SourcePosition(line=2, column=7), type=TokenType.COLON),
                Token(value=200, source_position=SourcePosition(line=2, column=8), type=TokenType.INT_CONST),
                Token(value='PLN', source_position=SourcePosition(line=2, column=12), type=TokenType.CURTYPE_CONST),
                Token(value='}', source_position=SourcePosition(line=3, column=1), type=TokenType.RIGHT_CURLY_BRACKET),
            ],
            DictConst(
                position=SourcePosition(line=1, column=1),
                pairs=[
                    Pair(
                        position=SourcePosition(line=1, column=2),
                        name='key',
                        expression=CurConst(position=SourcePosition(line=1, column=8), value=100, type='USD')
                    ),
                    Pair(
                        position=SourcePosition(line=2, column=2),
                        name='key2',
                        expression=CurConst(position=SourcePosition(line=2, column=8), value=200, type='PLN')
                    )
                ]
            )
        ),
        # Poprawne parsowanie pustego słownika
        (
            [
                Token(value='{', source_position=SourcePosition(line=1, column=1), type=TokenType.LEFT_CURLY_BRACKET),
                Token(value='}', source_position=SourcePosition(line=1, column=2), type=TokenType.RIGHT_CURLY_BRACKET),
            ],
            DictConst(position=SourcePosition(line=1, column=1), pairs=[])
        ),
        # Błędny token (brak zamykającej klamry)
        (
            [
                Token(value='{', source_position=SourcePosition(line=1, column=1), type=TokenType.LEFT_CURLY_BRACKET),
                Token(value='key', source_position=SourcePosition(line=1, column=2), type=TokenType.STR_CONST),
                Token(value=':', source_position=SourcePosition(line=1, column=7), type=TokenType.COLON),
                Token(value=100, source_position=SourcePosition(line=1, column=8), type=TokenType.INT_CONST),
                Token(value='USD', source_position=SourcePosition(line=1, column=12), type=TokenType.CURTYPE_CONST),
                Token(value='', source_position=SourcePosition(line=2, column=1), type=TokenType.END_OF_FILE),
            ],
            ParserError(
                "Expected RIGHT_CURLY_BRACKET, got END_OF_FILE while building dict.",
                SourcePosition(line=2, column=1)
                )
        ),
        # Błędny token (brak pary po przecinku)
        (
            [
                Token(value='{', source_position=SourcePosition(line=1, column=1), type=TokenType.LEFT_CURLY_BRACKET),
                Token(value='key', source_position=SourcePosition(line=1, column=2), type=TokenType.STR_CONST),
                Token(value=':', source_position=SourcePosition(line=1, column=7), type=TokenType.COLON),
                Token(value=100, source_position=SourcePosition(line=1, column=8), type=TokenType.INT_CONST),
                Token(value='USD', source_position=SourcePosition(line=1, column=12), type=TokenType.CURTYPE_CONST),
                Token(value=',', source_position=SourcePosition(line=1, column=15), type=TokenType.COMMA),
                Token(value=',', source_position=SourcePosition(line=2, column=1), type=TokenType.COMMA)
            ],
            ParserError("Expected a pair after \",\"", SourcePosition(line=2, column=1))
        ),
        # Błędny token (brak przecinka)
        (
            [
                Token(value='{', source_position=SourcePosition(line=1, column=1), type=TokenType.LEFT_CURLY_BRACKET),
                Token(value='key', source_position=SourcePosition(line=1, column=2), type=TokenType.STR_CONST),
                Token(value=':', source_position=SourcePosition(line=1, column=7), type=TokenType.COLON),
                Token(value=100, source_position=SourcePosition(line=1, column=8), type=TokenType.INT_CONST),
                Token(value='USD', source_position=SourcePosition(line=1, column=12), type=TokenType.CURTYPE_CONST),
                Token(value='key2', source_position=SourcePosition(line=2, column=2), type=TokenType.STR_CONST),
                Token(value=':', source_position=SourcePosition(line=2, column=7), type=TokenType.COLON),
                Token(value=200, source_position=SourcePosition(line=2, column=8), type=TokenType.INT_CONST),
                Token(value='PLN', source_position=SourcePosition(line=2, column=12), type=TokenType.CURTYPE_CONST),
                Token(value='}', source_position=SourcePosition(line=3, column=1), type=TokenType.RIGHT_CURLY_BRACKET),
            ],
            ParserError("Expected a comma before another pair.", SourcePosition(line=2, column=2))
        ),
    ])
    def test_parse_dict(self, tokens, expected_result):
        lexer = FakeLexer(tokens)
        parser = Parser(lexer)
        if isinstance(expected_result, ParserError):
            with pytest.raises(ParserError) as excinfo:
                parser._parse_dict()
            assert str(excinfo.value) == str(expected_result)
        else:
            result = parser._parse_dict()
            assert result == expected_result

    @pytest.mark.parametrize('tokens, expected_result', [
        # Poprawne parsowanie pary
        (
            [
                Token(value='key', source_position=SourcePosition(line=1, column=1), type=TokenType.STR_CONST),
                Token(value=':', source_position=SourcePosition(line=1, column=6), type=TokenType.COLON),
                Token(value=100, source_position=SourcePosition(line=1, column=7), type=TokenType.INT_CONST),
                Token(value='USD', source_position=SourcePosition(line=1, column=11), type=TokenType.CURTYPE_CONST),
            ],
            Pair(
                position=SourcePosition(line=1, column=1),
                name='key',
                expression=CurConst(position=SourcePosition(line=1, column=7), value=100, type='USD')
            )
        ),
        # Błędny token (brak dwukropka)
        (
            [
                Token(value='key', source_position=SourcePosition(line=1, column=1), type=TokenType.STR_CONST),
                Token(value=100, source_position=SourcePosition(line=1, column=6), type=TokenType.INT_CONST),
            ],
            ParserError("Expected COLON, got INT_CONST", SourcePosition(line=1, column=6))
        ),
    ])
    def test_parse_pair(self, tokens, expected_result):
        lexer = FakeLexer(tokens)
        parser = Parser(lexer)
        if isinstance(expected_result, ParserError):
            with pytest.raises(ParserError) as excinfo:
                parser._parse_pair()
            assert str(excinfo.value) == str(expected_result)
        else:
            result = parser._parse_pair()
            assert result == expected_result

    @pytest.mark.parametrize('tokens, expected_result', [
        # Poprawne parsowanie wyrażenia w nawiasach
        (
            [
                Token(value='(', source_position=SourcePosition(line=1, column=1), type=TokenType.LEFT_BRACKET),
                Token(value=42, source_position=SourcePosition(line=1, column=2), type=TokenType.INT_CONST),
                Token(value=')', source_position=SourcePosition(line=1, column=4), type=TokenType.RIGHT_BRACKET),
            ],
            IntConst(position=SourcePosition(line=1, column=2), value=42)
        ),
        # Brak wyrażenia w nawiasach
        (
            [
                Token(value='(', source_position=SourcePosition(line=1, column=1), type=TokenType.LEFT_BRACKET),
                Token(value=')', source_position=SourcePosition(line=1, column=2), type=TokenType.RIGHT_BRACKET),
            ],
            ParserError("Expected expression inside brackets", SourcePosition(line=1, column=2))
        ),
        # Brak zamykającego nawiasu
        (
            [
                Token(value='(', source_position=SourcePosition(line=1, column=1), type=TokenType.LEFT_BRACKET),
                Token(value=42, source_position=SourcePosition(line=1, column=2), type=TokenType.INT_CONST),
                Token(value='', source_position=SourcePosition(line=1, column=4), type=TokenType.END_OF_FILE),
            ],
            ParserError("Expected RIGHT_BRACKET, got END_OF_FILE", SourcePosition(line=1, column=4))
        ),
        # Błędny token początkowy (nie jest nawiasem otwierającym)
        (
            [
                Token(value='42', source_position=SourcePosition(line=1, column=1), type=TokenType.INT_CONST),
            ],
            None
        ),
    ])
    def test_parse_bracket_expression(self, tokens, expected_result):
        lexer = FakeLexer(tokens)
        parser = Parser(lexer)
        if isinstance(expected_result, ParserError):
            with pytest.raises(ParserError) as excinfo:
                parser._parse_bracket_expression()
            assert str(excinfo.value) == str(expected_result)
        else:
            result = parser._parse_bracket_expression()
            assert result == expected_result

    @pytest.mark.parametrize('tokens, expected_result', [
        # Poprawne parsowanie pojedynczego identyfikatora
        (
            [
                Token(value='obj', source_position=SourcePosition(line=1, column=1), type=TokenType.IDENTIFIER),
            ],
            ObjectAccess(
                position=SourcePosition(line=1, column=1),
                objects=[
                    IdentifierExpression(position=SourcePosition(line=1, column=1), name='obj')
                ]
            )
        ),
        # Poprawne parsowanie dostępu do obiektu z jedną kropką
        (
            [
                Token(value='obj', source_position=SourcePosition(line=1, column=1), type=TokenType.IDENTIFIER),
                Token(value='.', source_position=SourcePosition(line=1, column=4), type=TokenType.DOT),
                Token(value='field', source_position=SourcePosition(line=1, column=5), type=TokenType.IDENTIFIER),
            ],
            ObjectAccess(
                position=SourcePosition(line=1, column=1),
                objects=[
                    IdentifierExpression(position=SourcePosition(line=1, column=1), name='obj'),
                    IdentifierExpression(position=SourcePosition(line=1, column=5), name='field')
                ]
            )
        ),
        # Poprawne parsowanie dostępu do obiektu z wieloma kropkami
        (
            [
                Token(value='obj', source_position=SourcePosition(line=1, column=1), type=TokenType.IDENTIFIER),
                Token(value='.', source_position=SourcePosition(line=1, column=4), type=TokenType.DOT),
                Token(value='field', source_position=SourcePosition(line=1, column=5), type=TokenType.IDENTIFIER),
                Token(value='.', source_position=SourcePosition(line=1, column=10), type=TokenType.DOT),
                Token(value='method', source_position=SourcePosition(line=1, column=11), type=TokenType.IDENTIFIER),
                Token(value='(', source_position=SourcePosition(line=1, column=17), type=TokenType.LEFT_BRACKET),
                Token(value=')', source_position=SourcePosition(line=1, column=18), type=TokenType.RIGHT_BRACKET),
            ],
            ObjectAccess(
                position=SourcePosition(line=1, column=1),
                objects=[
                    IdentifierExpression(position=SourcePosition(line=1, column=1), name='obj'),
                    IdentifierExpression(position=SourcePosition(line=1, column=5), name='field'),
                    FunctionCall(position=SourcePosition(line=1, column=11), name='method', arguments=[]),
                ]
            )
        ),
        # Brak identyfikatora lub wywołania po kropce
        (
            [
                Token(value='obj', source_position=SourcePosition(line=1, column=1), type=TokenType.IDENTIFIER),
                Token(value='.', source_position=SourcePosition(line=1, column=4), type=TokenType.DOT),
                Token(value='', source_position=SourcePosition(line=1, column=5), type=TokenType.END_OF_FILE),

            ],
            ParserError("Expected identifier or call after \".\"", SourcePosition(line=1, column=5))
        ),
        # Nieprawidłowy początkowy token
        (
            [
                Token(value=42, source_position=SourcePosition(line=1, column=1), type=TokenType.INT_CONST),
            ],
            None
        ),
    ])
    def test_parse_object_access(self, tokens, expected_result):
        lexer = FakeLexer(tokens)
        parser = Parser(lexer)
        if isinstance(expected_result, ParserError):
            with pytest.raises(ParserError) as excinfo:
                parser._parse_object_access()
            assert str(excinfo.value) == str(expected_result)
        else:
            result = parser._parse_object_access()
            assert result == expected_result

    @pytest.mark.parametrize('tokens, expected_result', [
        # Poprawne parsowanie pojedynczego identyfikatora
        (
            [
                Token(value='foo', source_position=SourcePosition(line=1, column=1), type=TokenType.IDENTIFIER),
            ],
            IdentifierExpression(position=SourcePosition(line=1, column=1), name='foo')
        ),
        # Poprawne parsowanie wywołania funkcji bez argumentów
        (
            [
                Token(value='foo', source_position=SourcePosition(line=1, column=1), type=TokenType.IDENTIFIER),
                Token(value='(', source_position=SourcePosition(line=1, column=4), type=TokenType.LEFT_BRACKET),
                Token(value=')', source_position=SourcePosition(line=1, column=5), type=TokenType.RIGHT_BRACKET),
            ],
            FunctionCall(position=SourcePosition(line=1, column=1), name='foo', arguments=[])
        ),
        # Poprawne parsowanie wywołania funkcji z jednym argumentem
        (
            [
                Token(value='foo', source_position=SourcePosition(line=1, column=1), type=TokenType.IDENTIFIER),
                Token(value='(', source_position=SourcePosition(line=1, column=4), type=TokenType.LEFT_BRACKET),
                Token(value='arg', source_position=SourcePosition(line=1, column=5), type=TokenType.IDENTIFIER),
                Token(value=')', source_position=SourcePosition(line=1, column=8), type=TokenType.RIGHT_BRACKET),
            ],
            FunctionCall(
                position=SourcePosition(line=1, column=1),
                name='foo',
                arguments=[
                    ObjectAccess(
                        position=SourcePosition(line=1, column=5),
                        objects=[
                            IdentifierExpression(position=SourcePosition(line=1, column=5), name='arg')
                        ]
                    )
                ]
            )
        ),
        # Poprawne parsowanie wywołania funkcji z wieloma argumentami
        (
            [
                Token(value='foo', source_position=SourcePosition(line=1, column=1), type=TokenType.IDENTIFIER),
                Token(value='(', source_position=SourcePosition(line=1, column=4), type=TokenType.LEFT_BRACKET),
                Token(value='arg1', source_position=SourcePosition(line=1, column=5), type=TokenType.IDENTIFIER),
                Token(value=',', source_position=SourcePosition(line=1, column=9), type=TokenType.COMMA),
                Token(value='arg2', source_position=SourcePosition(line=1, column=11), type=TokenType.IDENTIFIER),
                Token(value=')', source_position=SourcePosition(line=1, column=15), type=TokenType.RIGHT_BRACKET),
            ],
            FunctionCall(position=SourcePosition(line=1, column=1), name='foo', arguments=[
                ObjectAccess(
                    position=SourcePosition(line=1, column=5),
                    objects=[
                        IdentifierExpression(position=SourcePosition(line=1, column=5), name='arg1'),
                    ]
                ),
                ObjectAccess(
                    position=SourcePosition(line=1, column=11),
                    objects=[
                        IdentifierExpression(position=SourcePosition(line=1, column=11), name='arg2')
                    ]
                )
            ])
        ),
        # Poprawne parsowanie wywołania funkcji z wieloma argumentami bez przecinka
        (
            [
                Token(value='foo', source_position=SourcePosition(line=1, column=1), type=TokenType.IDENTIFIER),
                Token(value='(', source_position=SourcePosition(line=1, column=4), type=TokenType.LEFT_BRACKET),
                Token(value='arg1', source_position=SourcePosition(line=1, column=5), type=TokenType.IDENTIFIER),
                Token(value='arg2', source_position=SourcePosition(line=1, column=11), type=TokenType.IDENTIFIER),
                Token(value=')', source_position=SourcePosition(line=1, column=15), type=TokenType.RIGHT_BRACKET),
            ],
            ParserError("Missing a comma betweem arguments.", SourcePosition(line=1, column=11))
        ),
        # Brak zamknięcia nawiasu w wywołaniu funkcji
        (
            [
                Token(value='foo', source_position=SourcePosition(line=1, column=1), type=TokenType.IDENTIFIER),
                Token(value='(', source_position=SourcePosition(line=1, column=4), type=TokenType.LEFT_BRACKET),
                Token(value='arg', source_position=SourcePosition(line=1, column=5), type=TokenType.IDENTIFIER),
                Token(value='', source_position=SourcePosition(line=1, column=8), type=TokenType.END_OF_FILE),
            ],
            ParserError("Expected RIGHT_BRACKET, got END_OF_FILE", SourcePosition(line=1, column=8))
        ),
        # Nieprawidłowy początkowy token
        (
            [
                Token(value=42, source_position=SourcePosition(line=1, column=1), type=TokenType.INT_CONST),
            ],
            None
        ),
    ])
    def test_parse_identifier_or_call(self, tokens, expected_result):
        lexer = FakeLexer(tokens)
        parser = Parser(lexer)
        if isinstance(expected_result, ParserError):
            with pytest.raises(ParserError) as excinfo:
                parser._parse_identifier_or_call()
            assert str(excinfo.value) == str(expected_result)
        else:
            result = parser._parse_identifier_or_call()
            assert result == expected_result

    @pytest.mark.parametrize('tokens, expected_result', [
        # Brak argumentów
        (
            [
                Token(value='.', source_position=SourcePosition(line=1, column=1), type=TokenType.DOT)
            ],
            []
        ),
        # Jeden argument
        (
            [
                Token(value='arg', source_position=SourcePosition(line=1, column=1), type=TokenType.IDENTIFIER)
            ],
            [
                ObjectAccess(
                    position=SourcePosition(line=1, column=1),
                    objects=[
                        IdentifierExpression(position=SourcePosition(line=1, column=1), name='arg')
                    ]
                )
            ]
        ),
        # Wiele argumentów
        (
            [
                Token(value='arg1', source_position=SourcePosition(line=1, column=1), type=TokenType.IDENTIFIER),
                Token(value=',', source_position=SourcePosition(line=1, column=5), type=TokenType.COMMA),
                Token(value='arg2', source_position=SourcePosition(line=1, column=7), type=TokenType.IDENTIFIER)
            ],
            [
                ObjectAccess(
                    position=SourcePosition(line=1, column=1),
                    objects=[
                        IdentifierExpression(position=SourcePosition(line=1, column=1), name='arg1'),
                    ]
                ),
                ObjectAccess(
                    position=SourcePosition(line=1, column=7),
                    objects=[
                        IdentifierExpression(position=SourcePosition(line=1, column=7), name='arg2')
                    ]
                )
            ]
        ),
        # Brak wyrażenia po przecinku
        (
            [
                Token(value='arg', source_position=SourcePosition(line=1, column=1), type=TokenType.IDENTIFIER),
                Token(value=',', source_position=SourcePosition(line=1, column=5), type=TokenType.COMMA),
                Token(value='', source_position=SourcePosition(line=1, column=6), type=TokenType.END_OF_FILE),
            ],
            ParserError("Expected expression after \",\"", SourcePosition(line=1, column=6))
        )
    ])
    def test_parse_arguments(self, tokens, expected_result):
        lexer = FakeLexer(tokens)
        parser = Parser(lexer)
        if isinstance(expected_result, ParserError):
            with pytest.raises(ParserError) as excinfo:
                parser._parse_arguments()
            assert str(excinfo.value) == str(expected_result)
        else:
            result = parser._parse_arguments()
            assert result == expected_result
