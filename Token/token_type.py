from enum import Enum, auto


class TokenType(Enum):

    # operators
    PLUS = auto()           # +
    MINUS = auto()          # -
    MUL = auto()            # *
    DIV = auto()            # /
    LESS = auto()           # <
    LESS_EQUAL = auto()     # <=
    GREATER = auto()        # >
    GREATER_EQUAL = auto()  # >=
    EQUAL = auto()          # ==
    NOT_EQUAL = auto()      # !=
    AND = auto()            # &&
    OR = auto()             # ||
    NOT = auto()            # !
    ASSIGN = auto()         # =
    ADD_AND_ASSIGN = auto()     # +=
    SUB_AND_ASSIGN = auto()     # -=
    CUR_TRANSFER = auto()   # ->

    # types
    INT = auto()
    FLOAT = auto()
    STR = auto()
    CUR = auto()
    CURTYPE = auto()
    DICT = auto()
    BOOL = auto()
    VOID = auto()

    BOOL_VALUE_TRUE = auto()    # true
    BOOL_VALUE_FALSE = auto()   # false

    STR_CONST = auto()
    IDENTIFIER = auto()
    INT_CONST = auto()
    FLOAT_CONST = auto()
    CURTYPE_CONST = auto()

    LEFT_BRACKET = auto()   # (
    RIGHT_BRACKET = auto()  # )
    DOT = auto()            # .
    COMMA = auto()          # ,
    LEFT_CURLY_BRACKET = auto()     # {
    RIGHT_CURLY_BRACKET = auto()    # }
    SEMICOLON = auto()      # ;
    COLON = auto()          # :

    # reserved names
    IF = auto()
    ELIF = auto()
    ELSE = auto()
    WHILE = auto()
    FOR = auto()
    IN = auto()
    RETURN = auto()
    FROM = auto()

    END_OF_FILE = auto()    # EOF
    COMMENT = auto()


BOOL_VALUE_MAPPING = {
    TokenType.BOOL_VALUE_TRUE: True,
    TokenType.BOOL_VALUE_FALSE: False
}
