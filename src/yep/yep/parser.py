from typing import List

from .ast import (
    AstNode,
    ExpressionNode,
    OperatorNode,
    NumberNode,
)

from .tokens import Token, TokenType, OPERATOR_TYPES


class Parser:
    """Converts tokens into an AST."""
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.errors: List[str] = []
        self._nodes: List[AstNode] = [] # The Ast Nodes we're building.
        self._pos = -1 # Index within the token list.
        self._value_queue: List[ExpressionNode] = []
        self._operator_stack: List[OperatorNode] = []

    def parse(self) -> List[AstNode]:
        while self._pos < len(self.tokens) - 1:
            self._pos += 1
            print(f'tokens={self.tokens} pos={self._pos}')
            token = self.tokens[self._pos]

            if token.token_type == TokenType.NUMBER:
                self._value_queue.append(NumberNode(value = token.literal))
                continue

            if token.token_type in OPERATOR_TYPES:
                self._operator_stack.append(OperatorNode(operator=token.token_type))
                continue

        print('end of parse')
        print('value stack: ', self._value_queue)
        print('operator stack: ', self._operator_stack)
        self._terminate_expression()
        return self._nodes

    def _terminate_expression(self):
        """Finish any expression that was pending."""
        while (len(self._operator_stack)):
            operator = self._operator_stack.pop()
            # Connect the operator to its operands.
            operator.operands = []
            arity = 2
            for operand in range(arity):
                operator.operands.append(self._value_queue.pop(0))

            self._nodes.append(operator)