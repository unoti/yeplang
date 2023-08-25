from dataclasses import dataclass
from typing import List, Union

from .tokens import TokenType

class AstNode:
    ...

@dataclass
class ExpressionNode(AstNode):
    ...

@dataclass
class OperatorNode(ExpressionNode):
    operator: TokenType
    operands: List[ExpressionNode] = None

@dataclass
class NumberNode(ExpressionNode):
    value: Union[int, float]