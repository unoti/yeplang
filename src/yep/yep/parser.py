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
        self._value_stack: List[ExpressionNode] = []
        self._operator_stack: List[OperatorNode] = []

    def parse(self) -> List[AstNode]:
        """Parse the tokens and create an AST.
        """
        print(f'parse tokens={self.tokens}')
        while self._pos < len(self.tokens) - 1:
            self._pos += 1
            token = self.tokens[self._pos]
            print(f'parse loop token={token} pos={self._pos}')

            if token.token_type == TokenType.NUMBER:
                self._value_stack.append(NumberNode(value = token.literal))
                continue

            if token.token_type in OPERATOR_TYPES:
                self._operator_stack.append(OperatorNode(operator=token.token_type))
                continue

        self._terminate_expression()
        return self._nodes

    def _terminate_expression(self):
        """Finish any expression that was pending.
        """
        print('terminate_expression')
        print('value stack: ', self._value_stack)
        print('operator stack: ', self._operator_stack)

        while (len(self._operator_stack)):
            operator = self._operator_stack.pop()
            # Connect the operator to its operands.
            operator.operands = []
            arity = 2
            for operand in range(arity):
                operator.operands.append(self._value_stack.pop())
            operator.operands.reverse() # Make sure the left operand stays on the left.

            # Now that the operation is "done" move it from the operator stack to the value stack.
            self._value_stack.append(operator)

        value = self._value_stack.pop()
        self._nodes.append(value)

