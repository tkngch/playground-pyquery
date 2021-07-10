from pyquery.logical_plan.expression.boolean.logical_boolean_expression import (
    LogicalBooleanExpression,
)
from pyquery.logical_plan.expression.logical_expression import LogicalExpression
from pyquery.logical_plan.logical_plan import LogicalPlan
from pyquery.physical_plan.expression.boolean.physical_lt import PhysicalLt
from pyquery.physical_plan.expression.physical_expression import PhysicalExpression


class LogicalLt(LogicalBooleanExpression):
    def __init__(self, left: LogicalExpression, right: LogicalExpression):
        super().__init__(name="lt", operator="<", left=left, right=right)

    def to_physical_expression(self, plan: LogicalPlan) -> PhysicalExpression:
        return PhysicalLt(
            left=self.left.to_physical_expression(plan),
            right=self.right.to_physical_expression(plan),
        )
