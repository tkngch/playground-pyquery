from pyquery.datatypes import ArrowTypes, Field
from pyquery.logical_plan.expression.logical_expression import LogicalExpression
from pyquery.logical_plan.logical_plan import LogicalPlan
from pyquery.physical_plan.expression.literal.physical_literal_long import (
    PhysicalLiteralLong,
)
from pyquery.physical_plan.expression.physical_expression import PhysicalExpression


class LogicalLiteralLong(LogicalExpression):
    def __init__(self, long: int):
        self.long = long

    def to_field(self, plan: LogicalPlan) -> Field:
        return Field(name=str(self.long), data_type=ArrowTypes.Int64)

    def to_string(self) -> str:
        return str(self.long)

    def to_physical_expression(self, plan: LogicalPlan) -> PhysicalExpression:
        return PhysicalLiteralLong(self.long)
