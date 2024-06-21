import sys
from Interpreter.reference import Reference
from Currency.currency import Currency, Curtype
from Interpreter.semantic_error import SemanticError


NUMBER_TYPES = [int, float]
STR_TYPES = [str]

NUMBER_RELATION_OPERATOR_MAPPING = {
    ">": lambda a, b: a > b,
    ">=": lambda a, b: a >= b,
    "<": lambda a, b: a < b,
    "<=": lambda a, b: a <= b,
    "==": lambda a, b: a == b,
    "!=": lambda a, b: a != b
}

CURTYPE_RELATION_OPERATOR_MAPPING = {
    "==": lambda a, b: a == b,
    "!=": lambda a, b: a != b
}

STRING_RELATION_OPERATOR_MAPPING = {
    "==": lambda a, b: a == b,
    "!=": lambda a, b: a != b
}

BOOL_RELATION_OPERATOR_MAPPING = {
    "==": lambda a, b: a is b,
    "!=": lambda a, b: a is not b
}


class Calculations:
    def __init__(self, exchange_rates):
        self._exchange_rates = exchange_rates

    def handle_bool_relations(self, left, right, expression, method):
        if type(left) is not bool or type(right) is not bool:
            raise SemanticError(f"Wrong type for operation, {type(left)} - {type(right)}", expression.position)
        return Reference(value=method(left, right))

    def compare_values(self, left, right, operator, relation):
        self._left = left
        self._right = right
        self._operator = operator

        result = self._try_compare_currency()
        if result is None:
            result = self._try_compare_numbers()
        if result is None:
            result = self._try_compare_strings()
        if result is None:
            result = self._try_compare_bools()
        if result is None:
            result = self._try_compare_curtype()

        if result is None:
            raise SemanticError(f"Wrong type for operation, {type(self._left)} - {type(self._right)}",
                                relation.position)

        return Reference(result)

    def negate_value(self, operator, right, expression):
        self._right = right
        result = None
        if operator == "!":
            result = self._try_negate_bool()
        else:
            result = self._try_negate_number() \
                or self._try_negate_currency(expression.position)

        if result is None:
            raise SemanticError(f"Wrong type for negation, {type(self._right)}", expression.position)

        return Reference(result)

    def calculate_result(self, left, right, expression, operation):
        self._left = left
        self._right = right
        self._position = expression.position
        if operation == "+":
            self._method = lambda a, b: a + b
            result = self._add_values()
        elif operation == "-":
            self._method = lambda a, b: a - b
            result = self._sub_values()
        elif operation == "*":
            self._method = lambda a, b: a * b
            result = self._mul_values()
        elif operation == "/":
            self._method = lambda a, b: a / b
            result = self._div_values()

        return Reference(result)

    def _check_number_size(self, value):
        if value > sys.maxsize or value < (-1) * sys.maxsize:
            raise ValueError("Value size exceeded")

    def _operate_on_currency(self):
        if (self._right.type != self._left.type):
            left_rate = self._exchange_rates.get(self._left.type.value)
            left_value = self._left.value / left_rate

            right_rate = self._exchange_rates.get(self._right.type.value)
            right_value = self._right.value / right_rate

            value = self._method(left_value, right_value)
            value = value * left_rate
            self._check_number_size(value)
            return Currency(value, self._left.type)

        value = self._method(self._left.value, self._right.value)
        self._check_number_size(value)
        return Currency(value, self._left.type)

    def _add_values(self):
        if type(self._left) in NUMBER_TYPES:
            value = self._left + self._right
            self._check_number_size(value)
            return value
        elif type(self._left) is str:
            return self._left + self._right
        else:
            return self._operate_on_currency()

    def _sub_values(self):
        if type(self._left) in NUMBER_TYPES:
            value = self._left - self._right
            self._check_number_size(value)
            return value
        else:
            return self._operate_on_currency()

    def _mul_values(self):
        if type(self._left) is Currency:
            value = self._left.value * self._right
            self._check_number_size(value)
            return Currency(value, self._left.type)
        elif type(self._right) is Currency:
            value = self._left * self._right.value
            self._check_number_size(value)
            return Currency(value, self._right.type)
        elif type(self._left) is str or type(self._right) is str:
            return self._left * self._right
        else:
            value = self._left * self._right
            self._check_number_size(value)
            return value

    def _div_values(self):
        if type(self._left) is float:
            value = self._left / self._right
            self._check_number_size(value)
            return value
        else:
            value = self._left.value / self._right
            self._check_number_size(value)
            return Currency(value, self._left.type)

    def _try_compare_currency(self):
        if not isinstance(self._left, Currency) or not isinstance(self._right, Currency):
            return None
        left_rate = self._exchange_rates.get(self._left.type.value)
        left_value = self._left.value / left_rate

        right_rate = self._exchange_rates.get(self._right.type.value)
        right_value = self._right.value / right_rate

        method = NUMBER_RELATION_OPERATOR_MAPPING.get(self._operator)
        return method(left_value, right_value)

    def _try_compare_numbers(self):
        if type(self._left) not in NUMBER_TYPES or type(self._right) not in NUMBER_TYPES:
            return None

        method = NUMBER_RELATION_OPERATOR_MAPPING.get(self._operator)
        return method(self._left, self._right)

    def _try_compare_curtype(self):
        if not isinstance(self._left, Curtype) or not isinstance(self._right, Curtype):
            return None

        method = CURTYPE_RELATION_OPERATOR_MAPPING.get(self._operator)
        if not method:
            return None

        return method(self._left.value, self._right.value)

    def _try_compare_strings(self):
        if type(self._left) not in STR_TYPES or type(self._right) not in STR_TYPES:
            return None

        method = STRING_RELATION_OPERATOR_MAPPING.get(self._operator)
        if not method:
            return None

        return method(self._left, self._right)

    def _try_compare_bools(self):
        if type(self._left) is not bool or type(self._right) is not bool:
            return None

        method = BOOL_RELATION_OPERATOR_MAPPING.get(self._operator)
        if not method:
            return None

        return method(self._left, self._right)

    def _try_negate_bool(self):
        if type(self._right) is not bool:
            return None
        return not self._right

    def _try_negate_number(self):
        if type(self._right) not in NUMBER_TYPES:
            return None
        return self._right * -1

    def _try_negate_currency(self, position):
        if not isinstance(self._right, Currency):
            return None
        return Currency(-self._right.value, self._right.type)
