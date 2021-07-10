from pyquery.datatypes import Field
from pyquery.logical_plan.expression.logical_expression import LogicalExpression
from pyquery.logical_plan.logical_plan import LogicalPlan
from pyquery.physical_plan.expression.physical_column import PhysicalColumn
from pyquery.physical_plan.expression.physical_expression import PhysicalExpression


class LogicalColumnIndex(LogicalExpression):
    def __init__(self, i: int):
        self.i = i

    def to_field(self, plan: LogicalPlan) -> Field:
        return plan.schema.fields[self.i]

    def to_string(self) -> str:
        return f"#{self.i}"

    def to_physical_expression(self, plan: LogicalPlan) -> PhysicalExpression:
        return PhysicalColumn(self.i)
