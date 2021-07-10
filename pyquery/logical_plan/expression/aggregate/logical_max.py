from pyquery.logical_plan.expression.aggregate.logical_aggregate_expression import (
    LogicalAggregateExpression,
)
from pyquery.logical_plan.expression.logical_expression import LogicalExpression
from pyquery.logical_plan.logical_plan import LogicalPlan
from pyquery.physical_plan.expression.aggregate.physical_aggregate_expression import (
    PhysicalAggregateExpression,
)
from pyquery.physical_plan.expression.aggregate.physical_max import PhysicalMax


class LogicalMax(LogicalAggregateExpression):
    def __init__(self, expression: LogicalExpression):
        super().__init__(name="MAX", expression=expression)

    def to_physical_expression(self, plan: LogicalPlan) -> PhysicalAggregateExpression:
        return PhysicalMax(self.expression.to_physical_expression(plan))
