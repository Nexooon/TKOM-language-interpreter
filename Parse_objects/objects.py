from dataclasses import dataclass
from typing import List, Dict, Optional, Union, Tuple, Callable
from typing_extensions import Self
from enum import Enum, auto

from Token.token_type import TokenType
from Source.source_position import SourcePosition


class DocumentObjectModel(Enum):
    INT = auto()
    FLOAT = auto()
    STR = auto()
    CUR = auto()
    CURTYPE = auto()
    BOOL = auto()
    DICT = auto()
    VOID = auto()


@dataclass
class Node:
    position: SourcePosition


@dataclass
class Expression(Node):
    left: Self
    right: Self

    def accept(self, visitor):
        visitor.visit_expression(self)


@dataclass
class OrExpression(Expression):
    def accept(self, visitor):
        visitor.visit_or_expression(self)


@dataclass
class AndExpression(Expression):
    def accept(self, visitor):
        visitor.visit_and_expression(self)


@dataclass
class LessRelation(Expression):
    def accept(self, visitor):
        visitor.visit_less_relation(self)


@dataclass
class LessEqualRelation(Expression):
    def accept(self, visitor):
        visitor.visit_less_equal_relation(self)


@dataclass
class GreaterRelation(Expression):
    def accept(self, visitor):
        visitor.visit_greater_relation(self)


@dataclass
class GreaterEqualRelation(Expression):
    def accept(self, visitor):
        visitor.visit_greater_equal_relation(self)


@dataclass
class EqualRelation(Expression):
    def accept(self, visitor):
        visitor.visit_equal_relation(self)


@dataclass
class NotEqualRelation(Expression):
    def accept(self, visitor):
        visitor.visit_not_equal_relation(self)


@dataclass
class NegatedExpression(Expression):
    def accept(self, visitor):
        visitor.visit_negated_expression(self)


@dataclass
class AddExpression(Expression):
    def accept(self, visitor):
        visitor.visit_add_expression(self)


@dataclass
class SubExpression(Expression):
    def accept(self, visitor):
        visitor.visit_sub_expression(self)


@dataclass
class MulExpression(Expression):
    def accept(self, visitor):
        visitor.visit_mul_expression(self)


@dataclass
class DivExpression(Expression):
    def accept(self, visitor):
        visitor.visit_div_expression(self)


@dataclass
class Literal(Node):
    ...


@dataclass
class IntConst(Literal):
    value: int

    def accept(self, visitor):
        visitor.visit_int_const(self)


@dataclass
class FloatConst(Literal):
    value: float

    def accept(self, visitor):
        visitor.visit_float_const(self)


@dataclass
class CurConst(Literal):
    value: Union[int, float]
    type: str

    def accept(self, visitor):
        visitor.visit_cur_const(self)


@dataclass
class StrConst(Literal):
    value: str

    def accept(self, visitor):
        visitor.visit_str_const(self)


@dataclass
class BoolConst(Literal):
    value: bool

    def accept(self, visitor):
        visitor.visit_bool_const(self)


@dataclass
class CurtypeConst(Literal):
    value: str

    def accept(self, visitor):
        visitor.visit_curtype_const(self)


@dataclass
class Pair(Node):
    name: str
    expression: Expression

    def accept(self, visitor):
        visitor.visit_pair(self)


@dataclass
class DictConst(Literal):
    pairs: List[Pair]

    def accept(self, visitor):
        visitor.visit_dict_const(self)


@dataclass
class IdentifierExpression(Node):
    name: str

    def accept(self, visitor):
        visitor.visit_identifier_expression(self)


@dataclass
class FunctionCall(IdentifierExpression):
    arguments: List[Expression]

    def accept(self, visitor):
        visitor.visit_function_call(self)


@dataclass
class Statement(Node):
    ...


@dataclass
class Block(Node):
    statements: List[Statement]

    def accept(self, visitor):
        visitor.visit_block(self)


@dataclass
class ObjectAccess(Statement):
    objects: List[Union[IdentifierExpression, FunctionCall]]

    def accept(self, visitor):
        visitor.visit_object_access(self)


@dataclass
class Declaration(Statement):
    type: DocumentObjectModel
    name: str

    def accept(self, visitor):
        visitor.visit_declaration(self)


@dataclass
class Assignment(Statement):
    object: Union[ObjectAccess, Declaration]
    expression: Expression

    def accept(self, visitor):
        visitor.visit_assignment(self)


@dataclass
class AddAndAssign(Statement):
    object: ObjectAccess
    expression: Expression

    def accept(self, visitor):
        visitor.visit_add_and_assign(self)


@dataclass
class SubAndAssign(Statement):
    object: ObjectAccess
    expression: Expression

    def accept(self, visitor):
        visitor.visit_sub_and_assign(self)


@dataclass
class IfStatement(Statement):
    condition: Expression
    block: Block
    elif_blocks: List[Tuple]
    else_block: Optional[Block] = None

    def accept(self, visitor):
        visitor.visit_if_statement(self)


@dataclass
class WhileLoopStatement(Statement):
    condition: Expression
    block: Block

    def accept(self, visitor):
        visitor.visit_while_loop_statement(self)


@dataclass
class ForLoopStatement(Statement):
    loop_identifier: str
    expression: Expression
    block: Block

    def accept(self, visitor):
        visitor.visit_for_loop_statement(self)


@dataclass
class ReturnStatement(Statement):
    expression: Expression

    def accept(self, visitor):
        visitor.visit_return_statement(self)


@dataclass
class CurrencyTransfer(Statement):
    expressions: List[Expression]

    def accept(self, visitor):
        visitor.visit_currency_transfer(self)


@dataclass
class BuiltInFunction(Node):
    name: str
    function: Callable

    def accept(self, visitor):
        visitor.visit_external_function(self)


@dataclass
class Parameter(Node):
    name: str
    type: DocumentObjectModel

    def accept(self, visitor):
        visitor.visit_parameter(self)


@dataclass
class FunctionDefinition(Node):
    name: str
    type: DocumentObjectModel
    params: List[Parameter]
    block: Block

    def accept(self, visitor):
        visitor.visit_function_definition(self)


@dataclass
class Program(Node):
    functions: Dict[str, FunctionDefinition]

    def accept(self, visitor):
        visitor.visit_program(self)


TYPES_MAPPING = {
    TokenType.INT: DocumentObjectModel.INT,
    TokenType.FLOAT: DocumentObjectModel.FLOAT,
    TokenType.STR: DocumentObjectModel.STR,
    TokenType.CUR: DocumentObjectModel.CUR,
    TokenType.CURTYPE: DocumentObjectModel.CURTYPE,
    TokenType.BOOL: DocumentObjectModel.BOOL,
    TokenType.DICT: DocumentObjectModel.DICT
}

FUNCTION_TYPES_MAPPING = {
    TokenType.INT: DocumentObjectModel.INT,
    TokenType.FLOAT: DocumentObjectModel.FLOAT,
    TokenType.STR: DocumentObjectModel.STR,
    TokenType.CUR: DocumentObjectModel.CUR,
    TokenType.CURTYPE: DocumentObjectModel.CURTYPE,
    TokenType.BOOL: DocumentObjectModel.BOOL,
    TokenType.DICT: DocumentObjectModel.DICT,
    TokenType.VOID: DocumentObjectModel.VOID
}


RELATION_OPERATOR_MAPPING = {
    TokenType.LESS: LessRelation,
    TokenType.LESS_EQUAL: LessEqualRelation,
    TokenType.GREATER: GreaterRelation,
    TokenType.GREATER_EQUAL: GreaterEqualRelation,
    TokenType.EQUAL: EqualRelation,
    TokenType.NOT_EQUAL: NotEqualRelation
}

ADDITIVE_OPERATOR_MAPPING = {
    TokenType.PLUS: AddExpression,
    TokenType.MINUS: SubExpression
}

MULTIPLICATIVE_OPERATOR_MAPPING = {
    TokenType.MUL: MulExpression,
    TokenType.DIV: DivExpression
}

ASSIGN_OPERATOR_MAPPING = {
    TokenType.ASSIGN: Assignment,
    TokenType.ADD_AND_ASSIGN: AddAndAssign,
    TokenType.SUB_AND_ASSIGN: SubAndAssign
}
