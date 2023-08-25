from dataclasses import dataclass
from enum import Enum
from typing import Optional, Union

class TokenType(str, Enum):
    # Single Character tokens
    LEFT_PAREN = '('
    RIGHT_PAREN = ')'
    LEFT_BRACE = '{'
    RIGHT_BRACE = '}'
    COMMA = ','
    DOT = '.'
    MINUS = '-'
    PLUS = '+'
    SEMICOLON = ';'
    SLASH = '/'
    STAR = '*'
    BANG = '!'
    EQUAL = '='
    LESS = '<'
    GREATER = '>'

    # 2 character tokens
    BANG_EQUAL = '!='
    EQUAL_EQUAL = '=='
    GREATER_EQUAL = '>='
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

SINGLE_CHARACTER_TOKENS = '(){},.-+;/*!=<>' # A concatenation of all possible single character tokens.
TWO_CHARACTER_TOKENS = ['!=', '==', '>=', '<=']

@dataclass
class Token:
    token_type: TokenType
    lexeme: str # The value of this token, the string of characters from the original source.
    line: int # Line number where this token was found
    col: int # Character number within the line
    literal: Optional[Union[str, int, float]] = None # The value this translates to.

def make_string(s: str):
    """Convenience function for making a literal string."""
    return Token(token_type = TokenType.STRING,
                 lexeme=s,
                 literal=s)

