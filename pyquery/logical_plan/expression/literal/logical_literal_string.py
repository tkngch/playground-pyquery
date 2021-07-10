from pyquery.datatypes import ArrowTypes, Field
from pyquery.logical_plan.expression.logical_expression import LogicalExpression
from pyquery.logical_plan.logical_plan import LogicalPlan
from pyquery.physical_plan.expression.literal.physical_literal_string import (
    PhysicalLiteralString,
)
from pyquery.physical_plan.expression.physical_expression import PhysicalExpression


class LogicalLiteralString(LogicalExpression):
    def __init__(self, string: str):
        self.string = string

    def to_field(self, plan: LogicalPlan) -> Field:
        return Field(name=self.string, data_type=ArrowTypes.String)

    def to_string(self) -> str:
        return f"'{self.string}'"

    def to_physical_expression(self, plan: LogicalPlan) -> PhysicalExpression:
        return PhysicalLiteralString(self.string)
