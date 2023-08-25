import string
from typing import Iterable

from yep.tokens import SINGLE_CHARACTER_TOKENS, Token, TokenType

class Scanner:
    def __init__(self, input: str):
        self.input = input
        self.pos = 0 # Offset within the full string for the current character.
        self.line = 1 # Line number within the input.
        self.col = 1 # Column number within the line.
    
    def tokens(self) -> Iterable[Token]:
        while self.pos < len(self.input):
            c = self.input[self.pos]

            if c in string.whitespace:
                pass
            elif c in SINGLE_CHARACTER_TOKENS:
                token_type = TokenType(c)
                token = Token(token_type=token_type, lexeme=c, line=self.line, col=self.col)
                yield token

            self.advance()

    def advance(self):
        self.pos += 1
        self.col += 1
        #*TODO: deal with advancing the line number and resetting the column.
