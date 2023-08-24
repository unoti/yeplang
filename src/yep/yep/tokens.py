from dataclasses import dataclass
from enum import Enum
from typing import Union

class TokenType(str, Enum):
    # Single Character tokens
    LEFT_PAREN = '('
    RIGHT_PAREN = ')'
    LEFT_BRACE = '{'
    RIGHT_BRACE = '}'
    COMMA = ','
    DOT = '.'
    MINUS = ','
    PLUS = '+'
    SEMICOLON = ';'
    SLASH = '/'
    STAR = '*'
    BANG = '!'
    BANG_EQUAL = '!='
    EQUAL = '='

    # 1-2 character tokens
    EQUAL_EQUAL = '=='
    GREATER = '>'
    GREATER_EQUAL = '>='
    LESS = '<'
    LESS_EQUAL = '<='

    # Literals
    IDENTIFIER = 'ident'
    STRING = 'string'
    NUMBER = 'num'

    # Keywords
    AND = 'and'
    CLASS = 'class'
    ELSE = 'else'
    FALSE = 'false'
    FUN = 'fun'
    FOR = 'for'
    IF = 'if'
    NIL = 'nil'
    OR = 'or'
    PRINT = 'print'
    RETURN = 'return'
    SUPER = 'super'
    THIS = 'this'
    TRUE = 'true'
    VAR = 'var'
    WHILE = 'while'

@dataclass
class Token:
    token_type: TokenType
    lexeme: str # The value of this token, the string of characters from the original source.
    literal: Union[str, int, float] # The value this translates to.
    line: int # Line number where this token was found
    pos: int # Character number within the line
