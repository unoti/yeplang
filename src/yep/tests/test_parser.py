from typing import List, Union
import unittest

from yep.ast import (
    AstNode,
    NumberNode,
    OperatorNode,
)
from yep.parser import Parser
from yep.scanner import Scanner
from yep.tokens import TokenType


class TestParser(unittest.TestCase):
    def setUp(self):
        self.diagnostic_output = False
        #self.diagnostic_output = True
    
    def test_expression_simple(self):
        ast = self._parse("1 + 2")
        print(ast)
        root = ast[0]
        self.assertTrue(isinstance(root, AstNode))
        self.assertTrue(isinstance(root, OperatorNode))
        opNode: OperatorNode = root
        self.assertEqual(opNode.operator, TokenType.PLUS)
        self.assertEqual(2, len(opNode.operands))       
        self._expect_operand(opNode.operands[0], TokenType.NUMBER, 1)
        self._expect_operand(opNode.operands[1], TokenType.NUMBER, 2)

    def _parse(self, input: str) -> List[AstNode]:
        scanner = Scanner(input)
        tokens = scanner.tokens()
        self.assertTrue(len(scanner.errors)==0, 'Scanner errors: '+str(scanner.errors))
        parser = Parser(tokens)
        ast = parser.parse()
        return ast

    def _expect_operand(self, node: AstNode, expected_token_type: TokenType, expected_value: Union[str, int, float]):
        if expected_token_type == TokenType.NUMBER:
            self.assertTrue(isinstance(node, NumberNode))
            self.assertEqual(expected_value, node.value)
        else:
            self.fail(f"Don't know how to validate token type {expected_token_type}")
