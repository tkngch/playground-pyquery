from pyquery.datatypes import ArrowTypes, Field
from pyquery.logical_plan.expression.logical_expression import LogicalExpression
from pyquery.logical_plan.logical_plan import LogicalPlan
from pyquery.physical_plan.expression.literal.physical_literal_double import (
    PhysicalLiteralDouble,
)
from pyquery.physical_plan.expression.physical_expression import PhysicalExpression


class LogicalLiteralDouble(LogicalExpression):
    def __init__(self, double: float) -> None:
        self.double = double

    def to_field(self, plan: LogicalPlan) -> Field:
        return Field(name=str(self.double), data_type=ArrowTypes.Double)

    def to_string(self) -> str:
        return str(self.double)

    def to_physical_expression(self, plan: LogicalPlan) -> PhysicalExpression:
        return PhysicalLiteralDouble(self.double)
