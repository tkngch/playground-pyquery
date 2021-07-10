from abc import ABC

from pyquery.datatypes import ArrowTypes, Field
from pyquery.logical_plan.expression.logical_binary_expression import (
    LogicalBinaryExpression,
)
from pyquery.logical_plan.logical_plan import LogicalPlan


class LogicalBooleanExpression(LogicalBinaryExpression, ABC):
    def to_field(self, plan: LogicalPlan) -> Field:
        return Field(name=self.name, data_type=ArrowTypes.Boolean)
