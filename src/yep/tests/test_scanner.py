from typing import List, Tuple, Union
import unittest

from yep.scanner import Scanner
from yep.tokens import Token, TokenType

class TestScanner(unittest.TestCase):
    def setUp(self):
        self.diagnostic_output = False
        #self.diagnostic_output = True

    def test_scanner_simple(self):
        self._expectTokens('+ -', [TokenType.PLUS, TokenType.MINUS])
        self._expectTokens('> >= < <=', [TokenType.GREATER, TokenType.GREATER_EQUAL, TokenType.LESS, TokenType.LESS_EQUAL])
    
    def test_numeric_literals(self):
        self._expectTokens('print 1 + 2',
                            [TokenType.PRINT, (TokenType.NUMBER, 1), TokenType.PLUS, (TokenType.NUMBER, 2)])
        self._expectTokens('print 123 + 456.7',
                            [TokenType.PRINT, (TokenType.NUMBER, 123), TokenType.PLUS, (TokenType.NUMBER, 456.7)])

    def test_string_literals(self):
        self._expectTokens('print "Hello, World!"',
                            [TokenType.PRINT, (TokenType.STRING, "Hello, World!")])
    
    #*TODO: error conditions to test
    # * unterminated string
    # * non-numerics after a number, like 123hello

    def x_test_identifiers(self):
        self._expectTokens('var x = 3',
                           [TokenType.VAR, (TokenType.IDENTIFIER, 'x'), TokenType.EQUAL, (TokenType.NUMBER, 3)])

        # Spaces should be optional.
        self._expectTokens('var x=3',
                           [TokenType.VAR, (TokenType.IDENTIFIER, 'x'), TokenType.EQUAL, (TokenType.NUMBER, 3)])

    def test_reserved_identifiers(self):
        """Edge cases with reserved words in identifiers."""
        # If there's a reserved word in the middle of an identifier that should be fine. "my_var"
        self._expectTokens('var my_var = 1',
                           [TokenType.VAR, (TokenType.IDENTIFIER, 'my_var'), TokenType.EQUAL, (TokenType.NUMBER, 1)])

        # If there's a reserved word at the start of an identifier that should be fine. "printer" ('print' is reserved)
        self._expectTokens('var printer = 1',
                           [TokenType.VAR, (TokenType.IDENTIFIER, 'printer'), TokenType.EQUAL, (TokenType.NUMBER, 1)])

    
    def _expectTokens(self, input: str, expectations: List[Union[TokenType, Tuple]]):
        """Verify that a string scans into what we expect.
        This is a convenience function to enable us to express the expectations in a compact, readable format.
        :param input: The string to scan.
        :param expectsions: A list of items, each of which can be either:
            - a single TokenType, which means we expect a token of this type (not a literal).
                -or-
            - a tuple of (TokenType, literal).
        """
        tokens = Scanner(input).tokens()
        if self.diagnostic_output:
            print(f'Input: {input}\nExpectation: {expectations}')
            print(f'Actuals: {tokens}')
        for seq, (expected_item, token) in enumerate(zip(expectations, tokens)):
            if self.diagnostic_output:
                print(f'seq={seq} expected_item={expected_item} token={token}')
            if isinstance(expected_item, TokenType):
                self.assertEqual(expected_item, token.token_type, f'For token number {seq} we expected {expected_item}')
            else:
                expected_token_type, expected_value = expected_item
                self.assertEqual(expected_token_type, token.token_type, f'For token {seq} we expected {expected_token_type}')
                if token.token_type in (TokenType.NUMBER, TokenType.STRING):
                    self.assertEqual(expected_value, token.literal, f'For token {seq} we expected {expected_value}')
                elif token.token_type == TokenType.IDENTIFIER:
                    self.assertEqual(expected_value, token.lexeme, f'For token {seq} unexpected identifier')
                else:
                    self.fail(f"We don't have a have to verify token type {expected_token_type}")
        self.assertEqual(len(expectations), len(tokens), f'We should have got back {len(expectations)} tokens')
        return tokens
