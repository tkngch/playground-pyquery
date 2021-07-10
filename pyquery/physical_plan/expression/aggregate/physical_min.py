from pyquery.physical_plan.expression.aggregate.accumulator import Accumulator
from pyquery.physical_plan.expression.aggregate.min_accumulator import MinAccumulator
from pyquery.physical_plan.expression.aggregate.physical_aggregate_expression import (
    PhysicalAggregateExpression,
)


class PhysicalMin(PhysicalAggregateExpression):
    def create_accumulator(self) -> Accumulator:
        return MinAccumulator()

    def to_string(self) -> str:
        return f"MIN({self.expression.to_string()})"
