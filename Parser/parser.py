from Parser.interface import Parser
from Parser.parser_error import ParserError
from Token.token_type import TokenType, BOOL_VALUE_MAPPING
from Source.source_position import SourcePosition
from Parse_objects.objects import (
    OrExpression,
    AndExpression,
    NegatedExpression,
    Assignment,
    Declaration,
    IntConst,
    FloatConst,
    CurConst,
    StrConst,
    BoolConst,
    CurtypeConst,
    Pair,
    DictConst,
    Block,
    IfStatement,
    WhileLoopStatement,
    ForLoopStatement,
    ReturnStatement,
    CurrencyTransfer,
    ObjectAccess,
    Parameter,
    IdentifierExpression,
    FunctionCall,
    FunctionDefinition,
    Program,
    TYPES_MAPPING,
    FUNCTION_TYPES_MAPPING,
    RELATION_OPERATOR_MAPPING,
    MULTIPLICATIVE_OPERATOR_MAPPING,
    ADDITIVE_OPERATOR_MAPPING,
    ASSIGN_OPERATOR_MAPPING
)


class Parser(Parser):
    types = TYPES_MAPPING
    function_types = FUNCTION_TYPES_MAPPING

    def __init__(self, lexer) -> None:
        self.lexer = lexer
        self.consume_token()

    def parse(self):
        return self._parse_program()

    def consume_token(self):
        self.token = self.lexer.get_next_token()
        if self.token.type == TokenType.COMMENT:
            self.consume_token()

    def _must_be(self, type: TokenType, additional_message=""):
        if self.token.type != type:
            raise ParserError(f"Expected {type.name}, got {self.token.type.name}{additional_message}",
                              self.token.position)
        value = self.token.value
        self.consume_token()
        return value

    # program = { function_definition }
    def _parse_program(self):
        functions = {}
        while (fun_def := self._parse_fun_def()):
            if old_fun := functions.get(fun_def.name):
                raise ParserError(f"Redefinition of a function from line {old_fun.position.line}", fun_def.position)
            functions[fun_def.name] = fun_def

        return Program(SourcePosition(1, 1), functions)

    # function_definition = function_type , identifier , "(" , parameters , ")" , block;
    def _parse_fun_def(self):
        if (type := self.function_types.get(self.token.type)) is None:
            return None

        position = self.token.position
        self.consume_token()
        name = self._must_be(TokenType.IDENTIFIER)
        self._must_be(TokenType.LEFT_BRACKET)
        params = self._parse_parameters()
        self._must_be(TokenType.RIGHT_BRACKET)
        block = self._parse_block()
        if not block:
            raise ParserError("Missing block of a defined function.", block.position)

        return FunctionDefinition(position, name, type, params, block)

    # parameters = [ parameter , { "," , parameter } ];
    def _parse_parameters(self):
        parameters = []
        if (parameter := self._parse_parameter()) is None:
            return parameters
        parameters.append(parameter)
        while self.token.type == TokenType.COMMA:
            self.consume_token()
            parameter = self._parse_parameter()
            if not parameter:
                raise ParserError("Expected a parameter after \",\"", self.token.position)
            parameters.append(parameter)

        return parameters

    # parameter = type , identifier;
    def _parse_parameter(self):
        if (type := self.types.get(self.token.type)) is None:
            return None
            # raise ParserError(f"Expected type, got {self.token.type.name}", self.token.position)
        position = self.token.position
        self.consume_token()
        name = self._must_be(TokenType.IDENTIFIER)

        return Parameter(position, name, type)

    # block = "{" , { statement } , "}";
    def _parse_block(self):
        if self.token.type != TokenType.LEFT_CURLY_BRACKET:
            return None
        position = self.token.position
        statements = []
        self.consume_token()
        while statement := self._parse_statement():
            statements.append(statement)
        self._must_be(TokenType.RIGHT_CURLY_BRACKET)

        return Block(position, statements)

    # statement = declaration
    #           | assignment_or_function_call
    #           | conditional
    #           | loop
    #           | return_statement
    #           | currency_transfer;
    def _parse_statement(self):
        statement = self._parse_declaration() \
            or self._parse_assignment_or_function_call() \
            or self._parse_conditional() \
            or self._parse_loop() \
            or self._parse_return_statement() \
            or self._parse_currency_transfer()

        return statement

    # declaration = type , identifier , [ "=" , expression ] , ";";
    def _parse_declaration(self):
        if (type := self.types.get(self.token.type)) is None:
            return None

        position = self.token.position
        self.consume_token()
        name = self._must_be(TokenType.IDENTIFIER)

        declatarion = Declaration(position, type, name)

        statement = self._parse_assign_declaration(declatarion, position) \
            or declatarion

        self._must_be(TokenType.SEMICOLON)

        return statement

    def _parse_assign_declaration(self, declaration, position):
        if self.token.type != TokenType.ASSIGN:
            return None

        self.consume_token()
        expression = self._parse_expression()
        if not expression:
            raise ParserError("Expected an expression after \"=\".", self.token.position)
        return Assignment(position, declaration, expression)

    # assignment_or_function_call = object_access , [ ( "=" | "+=" | "-=" ) , expression ] , ";";
    def _parse_assignment_or_function_call(self):
        position = self.token.position
        if (object_access := self._parse_object_access()) is None:
            return None

        if (statement := self._parse_object_assignment(object_access, position)) is None:
            statement = object_access
            if type(object_access.objects[-1]) is IdentifierExpression:
                raise ParserError("Expected assignment after identifier.", position)

        self._must_be(TokenType.SEMICOLON)

        return statement

    def _parse_object_assignment(self, object_access, position):
        if (operator_init := ASSIGN_OPERATOR_MAPPING.get(self.token.type)) is None:
            return None

        if type(object_access.objects[-1]) is FunctionCall:
            raise ParserError("Can't assign to function call", position)

        self.consume_token()
        expression = self._parse_expression()
        if not expression:
            raise ParserError("Expected an expression after assignment operation.", self.token.position)

        return operator_init(position, object_access, expression)

    # conditional = "if" , expression , block ,
    #             { "elif" , expression , block } ,
    #             [ "else" , block ];
    def _parse_conditional(self):
        if self.token.type != TokenType.IF:
            return None

        position = self.token.position
        self.consume_token()
        expression = self._parse_expression()
        if not expression:
            raise ParserError("Expected an expression after if.", self.token.position)

        block = self._parse_block()
        if not block:
            raise ParserError("Expected a block in if statement.", self.token.position)

        elif_blocks = []
        while self.token.type == TokenType.ELIF:
            self.consume_token()
            elif_expression = self._parse_expression()
            if not elif_expression:
                raise ParserError("Expected an expression after elif.", self.token.position)
            elif_block = self._parse_block()
            if not elif_block:
                raise ParserError("Expected a block after elif statement.", self.token.position)
            elif_blocks.append((elif_expression, elif_block))

        if self.token.type == TokenType.ELSE:
            self.consume_token()
            else_block = self._parse_block()
            if not else_block:
                raise ParserError("Expected a block after else statement", self.token.position)
            return IfStatement(position, expression, block, elif_blocks, else_block)

        return IfStatement(position, expression, block, elif_blocks)

    # loop = "while" , expression , block
    #      | "for" , identifier , "in" , identifier , block;
    def _parse_loop(self):
        loop = self._parse_while_loop() \
            or self._parse_for_loop()

        return loop

    # "while" , expression , block
    def _parse_while_loop(self):
        if self.token.type != TokenType.WHILE:
            return None

        position = self.token.position
        self.consume_token()
        expression = self._parse_expression()
        if not expression:
            raise ParserError("Expected expression after while", self.token.position)

        block = self._parse_block()
        if not block:
            raise ParserError("Expected block in while statement", self.token.position)

        return WhileLoopStatement(position, expression, block)

    # "for" , identifier , "in" , expression , block;
    def _parse_for_loop(self):
        if self.token.type != TokenType.FOR:
            return None

        position = self.token.position
        self.consume_token()
        loop_identifier = self._must_be(TokenType.IDENTIFIER, " while building for statement.")
        self._must_be(TokenType.IN)
        expression = self._parse_expression()
        if not expression:
            raise ParserError("Expected expression after \"in\".", self.token.position)
        block = self._parse_block()
        if not block:
            raise ParserError("Expected block in for statement", self.token.position)

        return ForLoopStatement(position, loop_identifier, expression, block)

    # return_statement = "return" , [ expression ] , ";";
    def _parse_return_statement(self):
        if self.token.type != TokenType.RETURN:
            return None

        position = self.token.position
        self.consume_token()
        expression = self._parse_expression()
        self._must_be(TokenType.SEMICOLON)

        return ReturnStatement(position, expression)

    # currency_transfer = "from" , expression , "->" , expression , [ "->" , expression ] , ";";
    def _parse_currency_transfer(self):
        if self.token.type != TokenType.FROM:
            return None

        position = self.token.position
        self.consume_token()
        expressions = []
        from_expression = self._parse_expression()
        if not from_expression:
            raise ParserError("Expected an expression after from keyword", self.token.position)
        expressions.append(from_expression)

        self._must_be(TokenType.CUR_TRANSFER)

        how_much_expression = self._parse_expression()
        if not how_much_expression:
            raise ParserError("Expected an expression after ->", self.token.position)
        expressions.append(how_much_expression)

        if self.token.type == TokenType.CUR_TRANSFER:
            self.consume_token()
            to_expression = self._parse_expression()
            if not to_expression:
                raise ParserError("Expected an expression after ->", self.token.position)
            expressions.append(to_expression)

        self._must_be(TokenType.SEMICOLON)

        if len(expressions) == 3:
            if type(expressions[0]) is not ObjectAccess or \
                    type(expressions[2]) is not ObjectAccess:
                raise ParserError("Wrong expressions types. Expected cur -> cur expression -> cur", position)
        else:
            if type(expressions[0]) is not ObjectAccess and type(expressions[1]) is not ObjectAccess:
                raise ParserError("Wrong expressions types. Expected cur -> cur_expression or cur_expression -> cur",
                                  position)
        return CurrencyTransfer(position, expressions)

    # expression = conjunction , { "||" , conjunction };
    def _parse_expression(self):
        if (left_factor := self._parse_conjunction()) is None:
            return None

        while self.token.type == TokenType.OR:
            position = self.token.position
            self.consume_token()
            right_factor = self._parse_conjunction()
            if right_factor is None:
                raise ParserError("Missing expression after ||.", position)
            left_factor = OrExpression(position, left_factor, right_factor)

        return left_factor

    # conjunction = negation , { "&&" , negation };
    def _parse_conjunction(self):
        if (left_factor := self._parse_negation()) is None:
            return None

        while self.token.type == TokenType.AND:
            position = self.token.position
            self.consume_token()
            right_factor = self._parse_negation()
            if right_factor is None:
                raise ParserError("Missing expression after &&.", position)
            left_factor = AndExpression(position, left_factor, right_factor)

        return left_factor

    # negation = [ "!" ] , relation_term;
    def _parse_negation(self):
        negated = False
        if self.token.type == TokenType.NOT:
            position = self.token.position
            negated = True
            self.consume_token()

        relation = self._parse_relation_term()
        if negated and not relation:
            raise ParserError("Expected expression after \"!\"", position)

        if not negated and not relation:
            return None

        return NegatedExpression(position, "!", relation) if negated else relation

    # relation_term = additive_term , [ relation_operator , additive_term ];
    def _parse_relation_term(self):
        if (left := self._parse_additive_term()) is None:
            return None

        position = self.token.position
        expression_init = RELATION_OPERATOR_MAPPING.get(self.token.type)
        if not expression_init:
            return left
        relation_type = self.token.type.name
        self.consume_token()
        right = self._parse_additive_term()
        if right is None:
            raise ParserError(f"Missing expression after {relation_type}.", position)

        return expression_init(position, left, right)

    # additive_term = multiplicative_term , { ( "+" | "-" ) , multiplicative_term };
    def _parse_additive_term(self):
        if (left := self._parse_multiplicative_term()) is None:
            return None

        while expression_init := ADDITIVE_OPERATOR_MAPPING.get(self.token.type):
            position = self.token.position
            operation_type = self.token.type.name
            self.consume_token()
            right = self._parse_multiplicative_term()
            if right is None:
                raise ParserError(f"Missing expression after {operation_type}.", position)
            left = expression_init(position, left, right)

        return left

    # multiplicative_term = unary_application , { ( "*" | "/" ) , unary_application };
    def _parse_multiplicative_term(self):
        if (left := self._parse_unary_application()) is None:
            return None

        while expression_init := MULTIPLICATIVE_OPERATOR_MAPPING.get(self.token.type):
            position = self.token.position
            operation_type = self.token.type.name
            self.consume_token()
            right = self._parse_unary_application()
            if right is None:
                raise ParserError(f"Missing expression after {operation_type}.", position)
            left = expression_init(position, left, right)

        return left

    # unary_application = [ "-" ] , term;
    def _parse_unary_application(self):
        negated = False
        if self.token.type == TokenType.MINUS:
            position = self.token.position
            negated = True
            self.consume_token()

        term = self._parse_term()
        if negated and not term:
            raise ParserError("Expected expression after \"-\"", position)

        if not negated and not term:
            return None

        return NegatedExpression(position, "-", term) if negated else term

    # term = literal | object_access | "(" , expression , ")";
    def _parse_term(self):
        term = self._parse_literal() \
            or self._parse_object_access() \
            or self._parse_bracket_expression()

        return term

    def _parse_literal(self):
        literal = self._parse_int_or_cur() \
            or self._parse_float_or_cur() \
            or self._parse_str() \
            or self._parse_bool() \
            or self._parse_curtype() \
            or self._parse_dict()

        return literal

    def _parse_int_or_cur(self):
        if self.token.type != TokenType.INT_CONST:
            return None

        position = self.token.position
        integer = IntConst(position, self.token.value)
        self.consume_token()

        if cur := self._parse_cur(position, integer.value):
            return cur

        return integer

    def _parse_float_or_cur(self):
        if self.token.type != TokenType.FLOAT_CONST:
            return None

        position = self.token.position
        float = FloatConst(position, self.token.value)
        self.consume_token()

        if cur := self._parse_cur(position, float.value):
            return cur

        return float

    def _parse_cur(self, position, number):
        if self.token.type != TokenType.CURTYPE_CONST:
            return None

        currency = CurConst(position, number, self.token.value)
        self.consume_token()

        return currency

    def _parse_str(self):
        if self.token.type != TokenType.STR_CONST:
            return None

        string = StrConst(self.token.position, self.token.value)
        self.consume_token()

        return string

    def _parse_bool(self):
        if (bool_value := BOOL_VALUE_MAPPING.get(self.token.type)) is None:
            return None

        boolean = BoolConst(self.token.position, bool_value)
        self.consume_token()

        return boolean

    def _parse_curtype(self):
        if self.token.type != TokenType.CURTYPE_CONST:
            return None

        curtype = CurtypeConst(self.token.position, self.token.value)
        self.consume_token()

        return curtype

    # dict = "{" , [ pair , { "," , pair } ] , "}";
    def _parse_dict(self):
        if self.token.type != TokenType.LEFT_CURLY_BRACKET:
            return None

        position = self.token.position
        self.consume_token()

        pairs = []

        if first_pair := self._parse_pair():
            pairs.append(first_pair)

            while self.token.type == TokenType.COMMA:
                self.consume_token()
                pair = self._parse_pair()
                if not pair:
                    raise ParserError("Expected a pair after \",\"", self.token.position)
                pairs.append(pair)

        if len(pairs) >= 1 and self.token.type == TokenType.STR_CONST:
            raise ParserError("Expected a comma before another pair.", self.token.position)

        self._must_be(TokenType.RIGHT_CURLY_BRACKET, " while building dict.")

        return DictConst(position, pairs)

    # pair = string , ":" , expression;
    def _parse_pair(self):
        if self.token.type != TokenType.STR_CONST:
            return None

        position = self.token.position
        name = self.token.value
        self.consume_token()

        self._must_be(TokenType.COLON)

        if (expression := self._parse_expression()) is None:
            raise ParserError("Expected cur after \":\"", self.token.position)

        return Pair(position, name, expression)

    def _parse_bracket_expression(self):
        if self.token.type != TokenType.LEFT_BRACKET:
            return None

        self.consume_token()
        expression = self._parse_expression()
        if not expression:
            raise ParserError("Expected expression inside brackets", self.token.position)
        self._must_be(TokenType.RIGHT_BRACKET)

        return expression

    # object_access = identifier_or_call , { "." , identifier_or_call };
    def _parse_object_access(self):
        position = self.token.position
        if (main_identifier_or_call := self._parse_identifier_or_call()) is None:
            return None

        identifiers_or_calls = [main_identifier_or_call]

        while self.token.type == TokenType.DOT:
            self.consume_token()
            identifier_or_call = self._parse_identifier_or_call()
            if not identifier_or_call:
                raise ParserError("Expected identifier or call after \".\"", self.token.position)
            identifiers_or_calls.append(identifier_or_call)

        return ObjectAccess(position, identifiers_or_calls)

    # identifier_or_call  = identifier , [ "(" , arguments , ")" ];
    def _parse_identifier_or_call(self):
        if self.token.type != TokenType.IDENTIFIER:
            return None

        position = self.token.position
        name = self.token.value
        self.consume_token()
        if self.token.type == TokenType.LEFT_BRACKET:
            self.consume_token()
            arguments = self._parse_arguments()
            if arguments and self.token.type == TokenType.IDENTIFIER:
                raise ParserError("Missing a comma betweem arguments.", self.token.position)
            self._must_be(TokenType.RIGHT_BRACKET)
            return FunctionCall(position, name, arguments)

        return IdentifierExpression(position, name)

    # arguments = [ expression , { "," , expression } ];
    def _parse_arguments(self):
        arguments = []
        if (expression := self._parse_expression()) is None:
            return arguments

        arguments.append(expression)
        while self.token.type == TokenType.COMMA:
            self.consume_token()
            expression = self._parse_expression()
            if not expression:
                raise ParserError("Expected expression after \",\"", self.token.position)
            arguments.append(expression)

        return arguments
