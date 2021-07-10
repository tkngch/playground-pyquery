from pyquery.logical_plan.expression.aggregate.logical_aggregate_expression import (
    LogicalAggregateExpression,
)
from pyquery.logical_plan.expression.logical_expression import LogicalExpression
from pyquery.logical_plan.logical_plan import LogicalPlan
from pyquery.physical_plan.expression.aggregate.physical_aggregate_expression import (
    PhysicalAggregateExpression,
)
from pyquery.physical_plan.expression.aggregate.physical_min import PhysicalMin


class LogicalMin(LogicalAggregateExpression):
    def __init__(self, expression: LogicalExpression):
        super().__init__(name="MIN", expression=expression)

    def to_physical_expression(self, plan: LogicalPlan) -> PhysicalAggregateExpression:
        return PhysicalMin(self.expression.to_physical_expression(plan))
