from abc import ABC

from pyquery.datatypes import Field
from pyquery.logical_plan.expression.logical_binary_expression import (
    LogicalBinaryExpression,
)
from pyquery.logical_plan.logical_plan import LogicalPlan


class LogicalMathExpression(LogicalBinaryExpression, ABC):
    def to_field(self, plan: LogicalPlan) -> Field:
        return Field(name=self.name, data_type=self.left.to_field(plan).data_type)
