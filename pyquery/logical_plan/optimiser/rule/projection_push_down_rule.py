from typing import FrozenSet, Tuple, Union

from pyquery.logical_plan.expression.aggregate.logical_aggregate_expression import (
    LogicalAggregateExpression,
)
from pyquery.logical_plan.expression.literal.logical_literal_double import (
    LogicalLiteralDouble,
)
from pyquery.logical_plan.expression.literal.logical_literal_long import (
    LogicalLiteralLong,
)
from pyquery.logical_plan.expression.literal.logical_literal_string import (
    LogicalLiteralString,
)
from pyquery.logical_plan.expression.logical_alias import LogicalAlias
from pyquery.logical_plan.expression.logical_binary_expression import (
    LogicalBinaryExpression,
)
from pyquery.logical_plan.expression.logical_column import LogicalColumn
from pyquery.logical_plan.expression.logical_column_index import LogicalColumnIndex
from pyquery.logical_plan.expression.logical_expression import LogicalExpression
from pyquery.logical_plan.logical_aggregate import LogicalAggregate
from pyquery.logical_plan.logical_plan import LogicalPlan
from pyquery.logical_plan.logical_projection import LogicalProjection
from pyquery.logical_plan.logical_scan import LogicalScan
from pyquery.logical_plan.logical_selection import LogicalSelection
from pyquery.logical_plan.optimiser.rule.optimiser_rule import OptimiserRule


class ProjectionPushDownRule(OptimiserRule):
    def optimise(self, plan: LogicalPlan) -> LogicalPlan:
        return self._push_down(plan, frozenset({}))

    def _push_down(
        self, plan: LogicalPlan, column_names: FrozenSet[str]
    ) -> LogicalPlan:
        if isinstance(plan, LogicalProjection):
            columns = self._extract_columns_from_multiple_expressions(
                plan.expressions, plan.plan, column_names
            )
            pushed_down = self._push_down(plan.plan, columns)
            return LogicalProjection(pushed_down, plan.expressions)

        if isinstance(plan, LogicalSelection):
            columns = self._extract_columns_from_single_expression(
                plan.expression, plan.plan
            )
            pushed_down = self._push_down(plan.plan, column_names.union(columns))
            return LogicalSelection(pushed_down, plan.expression)

        if isinstance(plan, LogicalAggregate):
            columns = column_names.union(
                self._extract_columns_from_multiple_expressions(
                    plan.group_expressions, plan.plan, frozenset({})
                ),
                self._extract_columns_from_multiple_expressions(
                    plan.aggregate_expressions, plan.plan, frozenset({})
                ),
            )
            pushed_down = self._push_down(plan.plan, columns)
            return LogicalAggregate(
                pushed_down, plan.group_expressions, plan.aggregate_expressions
            )

        if isinstance(plan, LogicalScan):
            return LogicalScan(plan.path, plan.data_source, tuple(sorted(column_names)))

        raise ValueError(f"ProjectPushDownRule does not support {plan.to_string()}")

    def _extract_columns_from_multiple_expressions(
        self,
        expressions: Tuple[Union[LogicalExpression, LogicalAggregateExpression], ...],
        plan: LogicalPlan,
        column_names: FrozenSet[str],
    ) -> FrozenSet[str]:
        return column_names.union(
            *[
                self._extract_columns_from_single_expression(expression, plan)
                for expression in expressions
            ]
        )

    def _extract_columns_from_single_expression(
        self,
        expression: Union[LogicalExpression, LogicalAggregateExpression],
        plan: LogicalPlan,
    ) -> FrozenSet[str]:
        if isinstance(expression, LogicalColumnIndex):
            return frozenset((plan.schema.fields[expression.i].name,))

        if isinstance(expression, LogicalColumn):
            return frozenset((expression.name,))

        if isinstance(expression, LogicalBinaryExpression):
            return self._extract_columns_from_single_expression(
                expression.left, plan
            ).union(
                self._extract_columns_from_single_expression(expression.right, plan)
            )

        if isinstance(expression, LogicalAlias):
            return self._extract_columns_from_single_expression(
                expression.expression, plan
            )

        if isinstance(expression, LogicalLiteralString):
            return frozenset({})

        if isinstance(expression, LogicalLiteralLong):
            return frozenset({})

        if isinstance(expression, LogicalLiteralDouble):
            return frozenset({})

        if isinstance(expression, LogicalAggregateExpression):
            return self._extract_columns_from_single_expression(
                expression.expression, plan
            )

        raise ValueError(
            f"_extract_columns does not support expression: {expression.to_string()}"
        )
