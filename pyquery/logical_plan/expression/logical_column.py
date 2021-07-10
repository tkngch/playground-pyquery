from pyquery.datatypes import Field
from pyquery.logical_plan.expression.logical_expression import LogicalExpression
from pyquery.logical_plan.logical_plan import LogicalPlan
from pyquery.physical_plan.expression.physical_column import PhysicalColumn
from pyquery.physical_plan.expression.physical_expression import PhysicalExpression


class LogicalColumn(LogicalExpression):
    def __init__(self, name: str):
        self.name = name

    def to_field(self, plan: LogicalPlan) -> Field:
        for field in plan.schema.fields:
            if field.name == self.name:
                return field

        raise ValueError(f"No column named '{self.name}'")

    def to_string(self) -> str:
        return f"#{self.name}"

    def to_physical_expression(self, plan: LogicalPlan) -> PhysicalExpression:
        for i, field in enumerate(plan.schema.fields):
            if field.name == self.name:
                return PhysicalColumn(i)

        raise ValueError(f"No column named '{self.name}'")
