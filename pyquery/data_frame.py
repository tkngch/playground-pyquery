from typing import Iterable, Tuple

from pyquery.datatypes.record_batch import RecordBatch
from pyquery.datatypes.schema import Schema
from pyquery.logical_plan.expression.aggregate.logical_aggregate_expression import (
    LogicalAggregateExpression,
)
from pyquery.logical_plan.expression.logical_expression import LogicalExpression
from pyquery.logical_plan.logical_aggregate import LogicalAggregate
from pyquery.logical_plan.logical_plan import LogicalPlan
from pyquery.logical_plan.logical_projection import LogicalProjection
from pyquery.logical_plan.logical_selection import LogicalSelection
from pyquery.logical_plan.optimiser.optimiser import Optimiser


class DataFrame:
    def __init__(self, plan: LogicalPlan) -> None:
        self._plan = plan

    def project(self, expressions: Tuple[LogicalExpression, ...]) -> "DataFrame":
        return DataFrame(LogicalProjection(self._plan, expressions))

    def filter(self, expression: LogicalExpression) -> "DataFrame":
        return DataFrame(LogicalSelection(self._plan, expression))

    def aggregate(
        self,
        group_by: Tuple[LogicalExpression, ...],
        aggregate_expressions: Tuple[LogicalAggregateExpression, ...],
    ) -> "DataFrame":
        return DataFrame(LogicalAggregate(self._plan, group_by, aggregate_expressions))

    @property
    def schema(self) -> Schema:
        return self._plan.schema

    @property
    def logical_plan(self) -> LogicalPlan:
        return self._plan

    def execute(self) -> Iterable[RecordBatch]:
        optimised_plan = Optimiser().optimise(self._plan)
        physical_plan = optimised_plan.to_physical_plan()
        return physical_plan.execute()
