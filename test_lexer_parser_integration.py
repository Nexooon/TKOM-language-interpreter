import io

import pytest

from Lexer.lexer import Lexer
from Parser.parser import Parser
from Source.source import SourceReader
from Source.source_position import SourcePosition
from Parse_objects.objects import DocumentObjectModel
from Parse_objects.objects import (
    Block,
    Parameter,
    FunctionDefinition,
    Program
)


class TestLexerParser:
    @pytest.mark.parametrize('source, expected_tree', [
        (
            'int fun(){}',
            Program(position=SourcePosition(line=1, column=1), functions={
                'fun': FunctionDefinition(
                    position=SourcePosition(line=1, column=1),
                    name='fun',
                    type=DocumentObjectModel.INT,
                    params=[],
                    block=Block(position=SourcePosition(line=1, column=10), statements=[])
                )
            })
        ),
        (
            'void fun(int x){}',
            Program(position=SourcePosition(line=1, column=1), functions={
                'fun': FunctionDefinition(
                    position=SourcePosition(line=1, column=1),
                    name='fun',
                    type=DocumentObjectModel.VOID,
                    params=[Parameter(position=SourcePosition(line=1, column=10), name='x',
                                      type=DocumentObjectModel.INT)],
                    block=Block(position=SourcePosition(line=1, column=16), statements=[])
                )
            })
        ),
        (
            'float fun(str x, int y, float z){}',
            Program(position=SourcePosition(line=1, column=1), functions={
                'fun': FunctionDefinition(
                    position=SourcePosition(line=1, column=1),
                    name='fun',
                    type=DocumentObjectModel.FLOAT,
                    params=[
                        Parameter(position=SourcePosition(line=1, column=11), name='x', type=DocumentObjectModel.STR),
                        Parameter(position=SourcePosition(line=1, column=18), name='y', type=DocumentObjectModel.INT),
                        Parameter(position=SourcePosition(line=1, column=25), name='z', type=DocumentObjectModel.FLOAT),
                    ],
                    block=Block(position=SourcePosition(line=1, column=33), statements=[])
                )
            })
        ),
    ])
    def test_function_definition(self, source, expected_tree):
        source = SourceReader(io.StringIO(source))
        lexer = Lexer(source)
        parser = Parser(lexer)
        assert parser.parse() == expected_tree
