import string
from typing import List

from yep.tokens import (
    SORTED_TOKEN_TYPES,
    Token,
    TokenType,
)

# Characters allowed in identifiers.
_ALLOWED_IN_IDENTIFIER = string.ascii_letters + string.digits + '_'

class Scanner:
    def __init__(self, input: str):
        self._input = input
        #*TODO: rework these positions to be encapsulated in a single structure. Probably include filename, too.
        self._pos = 0 # Offset within the full string for the current character.
        self._line = 1 # Line number within the input.
        self._col = 1 # Column number within the line.
        self._numeric_literal = '' # Any numeric literal we're currently building, stored as a string.
        self._string_literal = None # Any string literal we're currently building.
        self._identifier = None # Any identifier we're currently building.
        self._pending_tokens: List[Token] = [] # The list of tokens we're emitting.
    
    def tokens(self) -> List[Token]:
        while self._pos < len(self._input):
            c: str = self._input[self._pos]

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

            # Continue an existing string literal.
            if not self._string_literal is None:
                self._string_literal += c
                self._advance()
                continue

            if c in string.whitespace:
                self._terminate_identifier()
                self._terminate_numeric_literal()
                self._advance()
                continue

            # Continue an identifier.
            if self._identifier is not None and (c in _ALLOWED_IN_IDENTIFIER):
                self._identifier += c
                self._advance()
                continue

            # Continue an existing numeric literal, or start a new one.
            if str.isdigit(c) or (c=='.' and self._numeric_literal):
                self._numeric_literal += c
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
                self._terminate_identifier()
                self._pending_tokens.append(token)
                continue

            # Start an identifier.
            if self._identifier is None:
                self._identifier = c
            else:
                print(f'Syntax error "{c}" at line {self._line} col {self._col}')

            self._advance()

        # We have reached the end of the input.
        self._terminate_numeric_literal() # In case the source ends on a numeric literal.
        self._terminate_identifier()
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
        
        if s.isalnum():
            # When matching against reserved words, we must verify that there is not more letters afterwards
            # which would make it no longer a reserved word. For example 'variable' is not the reserved word 'var'.
            trailing_char = self._input[self._pos + len(s): self._pos + len(s) + 1]
            if trailing_char in _ALLOWED_IN_IDENTIFIER:
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

    def _terminate_identifier(self):
        """If we have been building an identifier then emit it now."""
        if self._identifier is None:
            return
        token = Token(TokenType.IDENTIFIER, lexeme=self._identifier,
                      line=self._line, col=self._col)
        self._pending_tokens.append(token)
        self._identifier = None
        