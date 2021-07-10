from pyquery.physical_plan.expression.aggregate.accumulator import Accumulator
from pyquery.physical_plan.expression.aggregate.avg_accumulator import AvgAccumulator
from pyquery.physical_plan.expression.aggregate.physical_aggregate_expression import (
    PhysicalAggregateExpression,
)


class PhysicalAvg(PhysicalAggregateExpression):
    def create_accumulator(self) -> Accumulator:
        return AvgAccumulator()

    def to_string(self) -> str:
        return f"AVG({self.expression.to_string()})"
