from pyquery.logical_plan.expression.logical_expression import LogicalExpression
from pyquery.logical_plan.expression.math.logical_math_expression import (
    LogicalMathExpression,
)
from pyquery.logical_plan.logical_plan import LogicalPlan
from pyquery.physical_plan.expression.math.physical_multiply import PhysicalMultiply
from pyquery.physical_plan.expression.physical_expression import PhysicalExpression


class LogicalMultiply(LogicalMathExpression):
    def __init__(self, left: LogicalExpression, right: LogicalExpression) -> None:
        super().__init__(name="multiply", operator="*", left=left, right=right)

    def to_physical_expression(self, plan: LogicalPlan) -> PhysicalExpression:
        return PhysicalMultiply(
            left=self.left.to_physical_expression(plan),
            right=self.right.to_physical_expression(plan),
        )
