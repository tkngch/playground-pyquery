from pyquery.datatypes import Field
from pyquery.logical_plan.expression.logical_expression import LogicalExpression
from pyquery.logical_plan.logical_plan import LogicalPlan
from pyquery.physical_plan.expression.physical_expression import PhysicalExpression


class LogicalAlias(LogicalExpression):
    def __init__(self, expression: LogicalExpression, alias: str):
        self.expression = expression
        self.alias_ = alias

    def to_field(self, plan: LogicalPlan) -> Field:
        return Field(self.alias_, self.expression.to_field(plan).data_type)

    def to_string(self) -> str:
        return f"{self.expression.to_string()} as {self.alias_}"

    def to_physical_expression(self, plan: LogicalPlan) -> PhysicalExpression:
        return self.expression.to_physical_expression(plan)
