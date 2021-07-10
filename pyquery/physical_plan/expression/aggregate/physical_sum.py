from pyquery.physical_plan.expression.aggregate.accumulator import Accumulator
from pyquery.physical_plan.expression.aggregate.physical_aggregate_expression import (
    PhysicalAggregateExpression,
)
from pyquery.physical_plan.expression.aggregate.sum_accumulator import SumAccumulator


class PhysicalSum(PhysicalAggregateExpression):
    def create_accumulator(self) -> Accumulator:
        return SumAccumulator()

    def to_string(self) -> str:
        return f"SUM({self.expression.to_string()})"
