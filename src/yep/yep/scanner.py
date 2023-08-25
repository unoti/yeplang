import string
from typing import List

from yep.tokens import (
    SORTED_TOKEN_TYPES,
    Token,
    TokenType,
)

class Scanner:
    def __init__(self, input: str):
        self._input = input
        #*TODO: rework these positions to be encapsulated in a single structure. Probably include filename, too.
        self._pos = 0 # Offset within the full string for the current character.
        self._line = 1 # Line number within the input.
        self._col = 1 # Column number within the line.
        self._numeric_literal = '' # Any numeric literal we're currently building, stored as a string.
        self._string_literal = None # Any string literal we're currently building.
        self._pending_tokens = []
    
    def tokens(self) -> List[Token]:
        while self._pos < len(self._input):
            c = self._input[self._pos]

            if c == '"':
                if self._string_literal is None:
                    # Start a new string literal.
                    self._string_literal = ''
                else:
                    # Terminate a string literal we started earlier.
                    token = Token(TokenType.STRING,
                                  lexeme=self._string_literal,
                                  line=self._line, col=self._col,
                                  literal=self._string_literal)
                    self._pending_tokens.append(token)
                    self._string_literal = None
                self._advance()
                continue

            if not self._string_literal is None:
                self._string_literal += c
                self._advance()
                continue

            if str.isdigit(c) or (c=='.' and self._numeric_literal):
                self._numeric_literal += c
                self._advance()
                continue

            if c in string.whitespace:
                self._terminate_numeric_literal()
                self._advance()
                continue

            # Look for tokens and reserved words starting at the current position,
            # looking for longer ones first.
            token = None
            for possible_token in SORTED_TOKEN_TYPES:
                if self._match(possible_token):
                    token = Token(token_type=TokenType(possible_token),
                                  lexeme=possible_token.value,
                                  line=self._line,
                                  col=self._col)
                    break
            if token:
                self._terminate_numeric_literal()
                self._pending_tokens.append(token)
                continue
    
            print(f'Unknown token at line {self._line} column {self._col} input={self._input} c="{c}"')
            self._advance()
        self._terminate_numeric_literal() # In case the source ends on a numeric literal.
        return self._pending_tokens

    def _advance(self):
        """Advance our position one character."""
        self._pos += 1
        self._col += 1
        #*TODO: deal with advancing the line number and resetting the column.

    def _peek(self, ahead_count: int = 1) -> str:
        """Return the next ahead_count characters from the current position without advancing."""
        return self._input[self._pos + 1: self._pos + 1 + ahead_count]

    def _match(self, s: str) -> bool:
        """Check to see if we have string `s` starting at the current position.
        If we do, return true and advance to the end of that string.
        """
        have = self._input[self._pos: self._pos + len(s)] # The input we have at this position to the desired length.
        if have != s:
            return False
        for i in range(len(s)):
            self._advance()
        return True
    
    def _terminate_numeric_literal(self):
        """If we've been working on a numeric literal then emit it now."""
        if not self._numeric_literal:
            return

        if '.' in self._numeric_literal:
            num = float(self._numeric_literal)
        else:
            num = int(self._numeric_literal)
        token = Token(TokenType.NUMBER,
                      lexeme=self._numeric_literal,
                      literal=num,
                      line=self._line,
                      col=self._col #*TODO: this should be the start of the literal not the end.
                    )
        self._pending_tokens.append(token)
        self._numeric_literal = '' # We no longer have a numeric literal pending.
