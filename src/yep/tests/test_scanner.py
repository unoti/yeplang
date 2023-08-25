from typing import List, Tuple, Union
import unittest

from yep.scanner import Scanner
from yep.tokens import Token, TokenType

class TestScanner(unittest.TestCase):
    def setUp(self):
        self.diagnostic_output = False
        #self.diagnostic_output = True

    def x_test_scanner_simple(self):
        self._expectTokens('+ -', [TokenType.PLUS, TokenType.MINUS])
        self._expectTokens('> >= < <=', [TokenType.GREATER, TokenType.GREATER_EQUAL, TokenType.LESS, TokenType.LESS_EQUAL])
    
    def x_test_numeric_literals(self):
        self._expectTokens('print 1 + 2',
                            [TokenType.PRINT, (TokenType.NUMBER, 1), TokenType.PLUS, (TokenType.NUMBER, 2)])
        self._expectTokens('print 123 + 456.7',
                            [TokenType.PRINT, (TokenType.NUMBER, 123), TokenType.PLUS, (TokenType.NUMBER, 456.7)])

    def test_scanner1(self):
        self._expectTokens('print "Hello, World!"',
                            [TokenType.PRINT, (TokenType.STRING, "Hello, World!")])
    
    #*TODO: verify we get an error on an unterminated string

    
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
                #*TODO: verify literals here.
                pass
        self.assertEqual(len(expectations), len(tokens), f'We should have got back {len(expectations)} tokens')
        return tokens
