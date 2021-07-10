from typing import Tuple

from pyquery.datatypes import Schema
from pyquery.logical_plan.expression.logical_expression import LogicalExpression
from pyquery.logical_plan.logical_plan import LogicalPlan
from pyquery.physical_plan.physical_plan import PhysicalPlan
from pyquery.physical_plan.physical_selection import PhysicalSelection


class LogicalSelection(LogicalPlan):
    """Plan to apply a filter expression."""

    def __init__(self, plan: LogicalPlan, expression: LogicalExpression):
        self.plan = plan
        self.expression = expression

    @property
    def schema(self) -> Schema:
        return self.plan.schema

    @property
    def children(self) -> Tuple[LogicalPlan, ...]:
        return (self.plan,)

    def to_string(self) -> str:
        return f"Selection: {self.expression.to_string()}"

    def to_physical_plan(self) -> PhysicalPlan:
        physical_plan = self.plan.to_physical_plan()
        physical_expr = self.expression.to_physical_expression(self.plan)
        return PhysicalSelection(plan=physical_plan, expression=physical_expr)
