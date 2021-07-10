from typing import Tuple

from pyquery.datatypes import Schema
from pyquery.logical_plan.expression.logical_expression import LogicalExpression
from pyquery.logical_plan.logical_plan import LogicalPlan
from pyquery.physical_plan.physical_plan import PhysicalPlan
from pyquery.physical_plan.physical_projection import PhysicalProjection


class LogicalProjection(LogicalPlan):
    """Plan to apply expressions to the input data."""

    def __init__(self, plan: LogicalPlan, expressions: Tuple[LogicalExpression, ...]):
        self.plan = plan
        self.expressions = expressions

    @property
    def schema(self) -> Schema:
        return Schema(tuple(expr.to_field(self.plan) for expr in self.expressions))

    @property
    def children(self) -> Tuple[LogicalPlan, ...]:
        return (self.plan,)

    def to_string(self) -> str:
        expr_string = ", ".join([expr.to_string() for expr in self.expressions])
        return f"Projection: {expr_string}"

    def to_physical_plan(self) -> PhysicalPlan:
        physical_plan = self.plan.to_physical_plan()
        physical_expr = tuple(
            expr.to_physical_expression(self.plan) for expr in self.expressions
        )
        schema = Schema(tuple(expr.to_field(self.plan) for expr in self.expressions))
        return PhysicalProjection(
            plan=physical_plan, schema=schema, expressions=physical_expr
        )
