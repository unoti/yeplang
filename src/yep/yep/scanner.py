import string
from typing import Iterable

from yep.tokens import (
    SINGLE_CHARACTER_TOKENS,
    Token,
    TokenType,
    TWO_CHARACTER_TOKENS
)

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
                self._advance()
                continue

            # Based on the concept of *maximal munch* let's try to build a 2 character lexeme first.
            token = None
            for possible_token in TWO_CHARACTER_TOKENS:
                if self._match(possible_token):
                    token = Token(token_type=TokenType(possible_token),
                                  lexeme=possible_token,
                                  line=self.line,
                                  col=self.col)
                    break
            if token:
                yield token
                continue

            # Since we didn't see any valid two character tokens it's now safe to check the single character tokens.
            if c in SINGLE_CHARACTER_TOKENS:
                token_type = TokenType(c)
                token = Token(token_type=token_type, lexeme=c, line=self.line, col=self.col)
                yield token
                self._advance()
                continue

    def _advance(self):
        """Advance our position one character."""
        self.pos += 1
        self.col += 1
        #*TODO: deal with advancing the line number and resetting the column.

    def _peek(self, ahead_count: int = 1) -> str:
        """Return the next ahead_count characters from the current position without advancing."""
        return self.input[self.pos + 1: self.pos + 1 + ahead_count]

    def _match(self, s: str) -> bool:
        """Check to see if we have string s starting at the current position.
        If we do, return true and advance to the end of that string.
        """
        have = self.input[self.pos: self.pos + len(s)] # The input we have at this position to the desired length.
        if have != s:
            return False
        for i in range(len(s)):
            self._advance()
        return True