from pyquery.datatypes import ArrowTypes, Field
from pyquery.logical_plan.expression.aggregate.logical_aggregate_expression import (
    LogicalAggregateExpression,
)
from pyquery.logical_plan.expression.logical_expression import LogicalExpression
from pyquery.logical_plan.logical_plan import LogicalPlan
from pyquery.physical_plan.expression.aggregate.physical_aggregate_expression import (
    PhysicalAggregateExpression,
)
from pyquery.physical_plan.expression.aggregate.physical_avg import PhysicalAvg


class LogicalAvg(LogicalAggregateExpression):
    def __init__(self, expression: LogicalExpression):
        super().__init__(name="AVG", expression=expression)

    def to_field(self, plan: LogicalPlan) -> Field:
        return Field(
            name=self.expression.to_field(plan).name, data_type=ArrowTypes.Double
        )

    def to_physical_expression(self, plan: LogicalPlan) -> PhysicalAggregateExpression:
        return PhysicalAvg(self.expression.to_physical_expression(plan))
