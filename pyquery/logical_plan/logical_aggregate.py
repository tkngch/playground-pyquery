from typing import Tuple

from pyquery.datatypes import Schema
from pyquery.logical_plan.expression.aggregate.logical_aggregate_expression import (
    LogicalAggregateExpression,
)
from pyquery.logical_plan.expression.logical_expression import LogicalExpression
from pyquery.logical_plan.logical_plan import LogicalPlan
from pyquery.physical_plan.physical_hash_aggregate import PhysicalHashAggregate
from pyquery.physical_plan.physical_plan import PhysicalPlan


class LogicalAggregate(LogicalPlan):
    """Plan to apply aggregate expressions."""

    def __init__(
        self,
        plan: LogicalPlan,
        group_expressions: Tuple[LogicalExpression, ...],
        aggregate_expressions: Tuple[LogicalAggregateExpression, ...],
    ):
        self.plan = plan
        self.group_expressions = group_expressions
        self.aggregate_expressions = aggregate_expressions

    @property
    def schema(self) -> Schema:
        return Schema(
            tuple(
                expression.to_field(self.plan)
                for expression in self.group_expressions + self.aggregate_expressions
            )
        )

    @property
    def children(self) -> Tuple[LogicalPlan, ...]:
        return (self.plan,)

    def to_string(self) -> str:
        group_expressions = ", ".join(
            [expression.to_string() for expression in self.group_expressions]
        )
        agg_expressions = ", ".join(
            [expression.to_string() for expression in self.aggregate_expressions]
        )
        return f"Aggregate: group-expressions=[{group_expressions}], aggregate-expressions=[{agg_expressions}]"

    def to_physical_plan(self) -> PhysicalPlan:
        physical_plan = self.plan.to_physical_plan()
        group_expressions = tuple(
            expr.to_physical_expression(self.plan) for expr in self.group_expressions
        )
        agg_expressions = tuple(
            expr.to_physical_expression(self.plan)
            for expr in self.aggregate_expressions
        )
        return PhysicalHashAggregate(
            plan=physical_plan,
            group_expressions=group_expressions,
            aggregate_expressions=agg_expressions,
            schema=self.schema,
        )
