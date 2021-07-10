from pyquery.physical_plan.expression.aggregate.accumulator import Accumulator
from pyquery.physical_plan.expression.aggregate.count_accumulator import (
    CountAccumulator,
)
from pyquery.physical_plan.expression.aggregate.physical_aggregate_expression import (
    PhysicalAggregateExpression,
)


class PhysicalCount(PhysicalAggregateExpression):
    def create_accumulator(self) -> Accumulator:
        return CountAccumulator()

    def to_string(self) -> str:
        return f"COUNT({self.expression.to_string()})"
