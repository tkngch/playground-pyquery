from pyquery.physical_plan.expression.aggregate.accumulator import Accumulator
from pyquery.physical_plan.expression.aggregate.max_accumulator import MaxAccumulator
from pyquery.physical_plan.expression.aggregate.physical_aggregate_expression import (
    PhysicalAggregateExpression,
)


class PhysicalMax(PhysicalAggregateExpression):
    def create_accumulator(self) -> Accumulator:
        return MaxAccumulator()

    def to_string(self) -> str:
        return f"MAX({self.expression.to_string()})"
