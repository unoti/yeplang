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

OPERATOR_TYPES = set([
    TokenType.MINUS, TokenType.PLUS, TokenType.SLASH, TokenType.STAR,
    TokenType.BANG, TokenType.EQUAL, TokenType.LESS, TokenType.GREATER,
    TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL, TokenType.GREATER_EQUAL,
    TokenType.LESS_EQUAL, TokenType.IDENTIFIER, TokenType.AND, TokenType.OR
])

# Items that are in the TokenType enum which are not reserved words and should be legal to use as identifiers.
_UNRESERVED_WORDS = [TokenType.IDENTIFIER, TokenType.STRING, TokenType.NUMBER]

# All token types sorted by length, with the longest ones first.
# We put the long tokens first for the concept of "maximal munch"--
# when it's ambiguous whether '<=' should be interpreted as ['<','='] vs ['<='] we prefer the bigger one.
# We exclude the literal types here because those are internal identifiers for the enum and not reserved words.
SORTED_TOKEN_TYPES = sorted([tt for tt in TokenType if tt not in _UNRESERVED_WORDS], key=lambda s: -len(s))

LITERAL_TYPES = [TokenType.STRING, TokenType.NUMBER]

@dataclass
class Token:
    token_type: TokenType
    lexeme: str # The value of this token, the string of characters from the original source.
    line: int # Line number where this token was found
    col: int # Character number within the line
    literal: Optional[Union[str, int, float]] = None # The value this translates to.

    def __repr__(self):
        if self.token_type in LITERAL_TYPES:
            return f'Token({self.token_type.value} {self.literal})'
        else:
            return f'Token({self.token_type.value})'