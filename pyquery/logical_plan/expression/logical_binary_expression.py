from abc import ABC

from pyquery.logical_plan.expression.logical_expression import LogicalExpression


class LogicalBinaryExpression(LogicalExpression, ABC):
    def __init__(
        self,
        name: str,
        operator: str,
        left: LogicalExpression,
        right: LogicalExpression,
    ) -> None:
        self.name = name
        self.operator = operator
        self.left = left
        self.right = right

    def to_string(self) -> str:
        return f"{self.left.to_string()} {self.operator} {self.right.to_string()}"
