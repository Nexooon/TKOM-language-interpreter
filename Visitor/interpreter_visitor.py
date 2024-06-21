from Visitor.interface import Visitor
from Context.context import Context
from Parse_objects.objects import BuiltInFunction, FunctionCall
from Interpreter.reference import Reference
from Interpreter.calculations import Calculations
from Currency.currency import Currency, Curtype, Dictionary
from Interpreter.semantic_error import SemanticError

from collections import deque

from Parse_objects.objects import DocumentObjectModel

TYPES_MAP = {
    DocumentObjectModel.INT: int,
    DocumentObjectModel.FLOAT: float,
    DocumentObjectModel.STR: str,
    DocumentObjectModel.CUR: Currency,
    DocumentObjectModel.CURTYPE: Curtype,
    DocumentObjectModel.BOOL: bool,
    DocumentObjectModel.DICT: Dictionary,
    DocumentObjectModel.VOID: None
}


class InterpreterVisitor(Visitor):
    def __init__(self, exchange_rates):
        self._last_result = None
        self._global_context = Context()
        self._call_context = Context(global_context=self._global_context)
        self._last_contexts = deque()
        self._calculations_handler = Calculations(exchange_rates)
        self._call_position = None
        self._returning = False
        self._declaring = False
        self._resolving = True

    def _consume_last_result(self):
        value = self._last_result
        self._last_result = None
        return value

    def _insert_builtin_functions(self):
        for function in BUILTINS_LIST:
            function_obj = BuiltInFunction(position=None, name=function[0], function=function[1])
            self._global_context.insert_symbol_function(function[0], function_obj)

    def _get_left_right_expressions(self, expression):
        expression.left.accept(self)
        left = self._consume_last_result()
        expression.right.accept(self)
        right = self._consume_last_result()
        return left, right

    def _call_function(self, function):
        self._last_contexts.append(self._call_context)
        self._call_context = Context(global_context=self._global_context)
        function.accept(self)
        self._call_context = self._last_contexts.pop()

    def visit_program(self, program):
        for function_name in program.functions:
            function = program.functions[function_name]
            self._global_context.insert_symbol_function(function_name, function)

        self._insert_builtin_functions()
        main_function = self._global_context.get_value_function('main')
        if not main_function:
            raise SemanticError("Missing main function.", program.position)
        if main_function.type is not DocumentObjectModel.VOID:
            raise SemanticError("Main function has to be void type", program.position)

        self._call_function(main_function)

    def visit_function_definition(self, function_definition):
        self._call_context.set_expected_return_type(TYPES_MAP[function_definition.type])
        arguments = self._consume_last_result() or []
        if len(arguments) != len(function_definition.params):
            raise SemanticError(f"Wrong amount of arguments, expected {len(function_definition.params)}\
                                , got {len(arguments)}", self._call_position)

        for argument, parameter in zip(arguments, function_definition.params):
            if type(argument.value) is not TYPES_MAP[parameter.type]:
                raise SemanticError("Parameter type mismatch.", self._call_position)
            self._call_context.insert_symbol_variable(parameter.name, argument)

        function_definition.block.accept(self)

        self._returning = False

    def visit_block(self, block):
        self._call_context.enter_scope()
        for statement in block.statements:
            statement.accept(self)
            if self._returning:
                break
            self._declaring = False
            self._last_result = None
        self._call_context.leave_scope()

    def visit_function_call(self, fun_call):
        arguments = []
        self._call_position = fun_call.position
        for argument in fun_call.arguments:
            argument.accept(self)
            value = self._consume_last_result()
            arguments.append(value if isinstance(value, Reference) else Reference(value))
        self._last_result = arguments
        function = self._global_context.get_value_function(fun_call.name)
        if function is None:
            raise SemanticError(f"Function {fun_call.name} not found", fun_call.position)
        self._call_function(function)

    def visit_external_function(self, built_in_function):
        arguments = self._consume_last_result() or []
        try:
            self._last_result = built_in_function.function(*[argument.value for argument in arguments]
                                                           if len(arguments) else " ")
        except Exception as e:
            raise SemanticError(e.args[0], self._call_position)

    def visit_object_access(self, object_access):
        object_access.objects[0].accept(self)
        if len(object_access.objects) == 1:
            return

        method_or_value = self._consume_last_result().value
        for part in object_access.objects[1:]:
            if type(part) is FunctionCall:
                args = part.arguments
                args_values = []
                for arg in args:
                    arg.accept(self)
                    args_values.append(self._consume_last_result().value)
                method = getattr(method_or_value, part.name)
                ret = method(*args_values)
                if ret:
                    self._last_result = Reference(ret)
                    break
            else:
                method_or_value_name = part.name
                method_or_value = getattr(method_or_value, method_or_value_name)

            self._last_result = Reference(method_or_value)

    def visit_identifier_expression(self, identifier_expression):
        if self._resolving:
            value_obj = self._call_context.get_value_variable(identifier_expression.name) or \
                self._call_context.get_value_function(identifier_expression.name)
            if value_obj is None:
                raise SemanticError(f"'{identifier_expression.name}' was not declared in this scope",
                                    identifier_expression.position)
            self._last_result = value_obj
        else:
            self._last_result = identifier_expression.name

    def visit_declaration(self, declaration):
        self._declaring = True
        if (self._call_context.get_current_scope_value_variable(declaration.name)) is not None:
            raise SemanticError(f"Redeclaration of a variable {declaration.name}", declaration.position)
        self._last_result = declaration

    def visit_assignment(self, assignment):
        self._resolving = False
        assignment.object.accept(self)
        object = self._consume_last_result()
        self._resolving = True
        assignment.expression.accept(self)
        value = self._consume_last_result()
        value = value.value if isinstance(value, Reference) else value

        if self._declaring:
            if type(value) is not TYPES_MAP[object.type]:
                raise SemanticError("Type mismatch.", assignment.position)
            self._call_context.insert_symbol_variable(
                object.name, value if isinstance(value, Reference) else Reference(value)
            )
        else:
            old_value = self._call_context.get_value_variable(object)
            if old_value is None:
                raise SemanticError("Undefined variable.", assignment.position)
            if type(value) is not type(old_value.value):
                raise SemanticError(f"Type mismatch, {type(old_value.value)} - {type(value)}", assignment.position)
            old_value.value = value

    def _operate_and_assign(self, assignment, method):
        self._resolving = False
        assignment.object.accept(self)
        object = self._consume_last_result()
        self._resolving = True

        assignment.expression.accept(self)
        value = self._consume_last_result()
        value = value.value if isinstance(value, Reference) else value

        old_value = self._call_context.get_value_variable(object)
        if old_value is None:
            raise SemanticError(f"Undefined variable {object}", assignment.position)
        if type(value) is not type(old_value.value):
            raise SemanticError(f"Type mismatch, {type(old_value.value)} - {type(value)}", assignment.position)

        if method == "+":
            old_value.value += value
        else:
            old_value.value -= value

    def visit_add_and_assign(self, assignment):
        self._operate_and_assign(assignment, "+")

    def visit_sub_and_assign(self, assignment):
        self._operate_and_assign(assignment, "-")

    def visit_if_statement(self, if_statement):
        if_statement.condition.accept(self)
        if self._consume_last_result().value:
            if_statement.block.accept(self)
        else:
            elif_completed = False
            for elif_block in if_statement.elif_blocks:
                elif_block[0].accept(self)
                if self._consume_last_result().value:
                    elif_block[1].accept(self)
                    elif_completed = True
                    break
            if if_statement.else_block and not elif_completed:
                if_statement.else_block.accept(self)

    def visit_while_loop_statement(self, while_statement):
        while_statement.condition.accept(self)
        execute = self._consume_last_result()
        while execute.value:
            while_statement.block.accept(self)
            if self._returning:
                break
            while_statement.condition.accept(self)
            execute = self._consume_last_result()

    def visit_for_loop_statement(self, for_statement):
        for_statement.expression.accept(self)
        iterable = self._consume_last_result()
        for element in iterable.value:
            self._call_context.insert_symbol_variable(for_statement.loop_identifier, element)
            for_statement.block.accept(self)
            if self._returning:
                break

    def visit_return_statement(self, return_statement):
        if return_statement.expression:
            return_statement.expression.accept(self)
            return_value = self._consume_last_result()
            expected = self._call_context.get_expected_return_type()
            if type(return_value.value) is not expected:
                raise SemanticError(f"Wrong return type, expected {expected}, got {type(return_value.value)}",
                                    return_statement.position)
            return_statement.expression.accept(self)
        else:
            expected = self._call_context.get_expected_return_type()
            if expected is not None:
                raise SemanticError(f"Expected return of a type {expected}", return_statement.position)
        self._returning = True

    def visit_currency_transfer(self, currency_transfer):
        expressions = []
        for expression in currency_transfer.expressions:
            expression.accept(self)
            currency = self._consume_last_result()
            expressions.append(currency)

        for expression in expressions:
            if type(expression.value) is not Currency:
                raise SemanticError("Expected a cur expressions in transfer", currency_transfer.position)

        if len(currency_transfer.expressions) == 3:
            new_currency_from = self._calculations_handler.calculate_result(
                expressions[0].value,
                expressions[1].value,
                currency_transfer, "-")
            expressions[0].value = new_currency_from.value

            new_currency_to = self._calculations_handler.calculate_result(
                expressions[2].value,
                expressions[1].value,
                currency_transfer, "+")
            expressions[2].value = new_currency_to.value

        else:
            new_currency_to = self._calculations_handler.calculate_result(
                expressions[1].value,
                expressions[0].value,
                currency_transfer, "+")

            new_currency_from = self._calculations_handler.calculate_result(
                expressions[0].value,
                expressions[1].value,
                currency_transfer, "-")
            expressions[1].value = new_currency_to.value
            expressions[0].value = new_currency_from.value

    def visit_expression(self, expression):
        ...

    def visit_or_expression(self, or_expression):
        or_expression.left.accept(self)
        left = self._consume_last_result()
        if left.value is True:
            self._last_result = Reference(True)
            return
        or_expression.right.accept(self)
        right = self._consume_last_result()
        self._last_result = self._calculations_handler.handle_bool_relations(
            left.value, right.value, or_expression, lambda a, b: a or b
        )

    def visit_and_expression(self, and_expression):
        and_expression.left.accept(self)
        left = self._consume_last_result()
        if left.value is False:
            self._last_result = Reference(False)
            return
        and_expression.right.accept(self)
        right = self._consume_last_result()
        self._last_result = self._calculations_handler.handle_bool_relations(
            left.value, right.value, and_expression, lambda a, b: a and b
        )

    def visit_less_relation(self, relation):
        left, right = self._get_left_right_expressions(relation)
        self._last_result = self._calculations_handler.compare_values(left.value, right.value, "<", relation)

    def visit_less_equal_relation(self, relation):
        left, right = self._get_left_right_expressions(relation)
        self._last_result = self._calculations_handler.compare_values(left.value, right.value, "<=", relation)

    def visit_greater_relation(self, relation):
        left, right = self._get_left_right_expressions(relation)
        self._last_result = self._calculations_handler.compare_values(left.value, right.value, ">", relation)

    def visit_greater_equal_relation(self, relation):
        left, right = self._get_left_right_expressions(relation)
        self._last_result = self._calculations_handler.compare_values(left.value, right.value, ">=", relation)

    def visit_equal_relation(self, relation):
        left, right = self._get_left_right_expressions(relation)
        self._last_result = self._calculations_handler.compare_values(left.value, right.value, "==", relation)

    def visit_not_equal_relation(self, relation):
        left, right = self._get_left_right_expressions(relation)
        self._last_result = self._calculations_handler.compare_values(left.value, right.value, "!=", relation)

    def visit_negated_expression(self, negation):
        negation.right.accept(self)
        right = self._consume_last_result()
        self._last_result = self._calculations_handler.negate_value(negation.left, right.value, negation)

    def visit_add_expression(self, expression):
        left, right = self._get_left_right_expressions(expression)

        acceptable_right_type = ADD_TYPES.get(type(left.value), None)
        if acceptable_right_type is None or type(right.value) not in acceptable_right_type:
            raise SemanticError("Different types in add operation", expression.position)

        self._last_result = self._calculations_handler.calculate_result(
            left.value, right.value, expression, "+"
        )

    def visit_sub_expression(self, expression):
        left, right = self._get_left_right_expressions(expression)

        acceptable_right_type = SUB_TYPES.get(type(left.value), None)
        if acceptable_right_type is None or type(right.value) not in acceptable_right_type:
            raise SemanticError("Different types in sub operation", expression.position)

        self._last_result = self._calculations_handler.calculate_result(
            left.value, right.value, expression, "-"
        )

    def visit_mul_expression(self, expression):
        left, right = self._get_left_right_expressions(expression)

        acceptable_right_type = MUL_TYPES.get(type(left.value), None)
        if acceptable_right_type is None or type(right.value) not in acceptable_right_type:
            raise SemanticError("Different types in multiply operation", expression.position)

        self._last_result = self._calculations_handler.calculate_result(
            left.value, right.value, expression, "*"
        )

    def visit_div_expression(self, expression):
        left, right = self._get_left_right_expressions(expression)

        acceptable_right_type = DIV_TYPES.get(type(left.value), None)
        if acceptable_right_type is None or type(right.value) not in acceptable_right_type:
            raise SemanticError("Wrong types in divide operation", expression.position)

        self._last_result = self._calculations_handler.calculate_result(
            left.value, right.value, expression, "/"
        )

    def visit_int_const(self, const):
        self._last_result = Reference(const.value)

    def visit_float_const(self, const):
        self._last_result = Reference(const.value)

    def visit_cur_const(self, const):
        type = Curtype(const.type)
        self._last_result = Reference(Currency(const.value, type))

    def visit_str_const(self, const):
        self._last_result = Reference(const.value)

    def visit_bool_const(self, const):
        self._last_result = Reference(const.value)

    def visit_curtype_const(self, const):
        self._last_result = Reference(Curtype(const.value))

    def visit_dict_const(self, dict):
        dictionary = Dictionary({})
        for pair in dict.pairs:
            name = pair.name
            pair.expression.accept(self)
            expression = self._consume_last_result()
            if type(expression.value) is not Currency:
                raise SemanticError("Expected cur in dict value", dict.position)

            if dictionary.storage.get(name):
                raise SemanticError(f"Multiple account name '{name}' defined", dict.position)
            dictionary.storage[name] = expression.value
        self._last_result = Reference(dictionary)


def print_(text):
    print(text)


def input_(text):
    value = input(text)
    return value


def to_int(value):
    if type(value) not in [float, str]:
        raise TypeError("Can convert only float or str")
    try:
        return Reference(int(value))
    except Exception:
        raise ValueError("Wrong value to convert")


def to_float(value):
    if type(value) not in [int, str]:
        raise TypeError("Can convert only int or str")
    try:
        return Reference(float(value))
    except Exception:
        raise ValueError("Wrong value to convert")


def to_str(value):
    if type(value) not in [int, float, Currency, Curtype]:
        raise TypeError("Can convert only int, float, cur or curtype")
    try:
        return Reference(str(value))
    except Exception:
        raise ValueError("Wrong value to convert")


BUILTINS_LIST = [
    ('print', print_),
    ('input', input_),
    ('to_int', to_int),
    ('to_float', to_float),
    ('to_str', to_str)
]

ADD_TYPES = {
    int: [int],
    float: [float],
    str: [str],
    Currency: [Currency]
}

SUB_TYPES = {
    int: [int],
    float: [float],
    Currency: [Currency]
}

MUL_TYPES = {
    int: [int, str, Currency],
    float: [float, Currency],
    str: [int],
    Currency: [int, float]
}

DIV_TYPES = {
    float: [float],
    Currency: [int, float]
}
