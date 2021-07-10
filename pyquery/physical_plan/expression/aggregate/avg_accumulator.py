from typing import Any, Optional

from pyquery.physical_plan.expression.aggregate.accumulator import Accumulator
from pyquery.physical_plan.expression.aggregate.count_accumulator import (
    CountAccumulator,
)
from pyquery.physical_plan.expression.aggregate.sum_accumulator import SumAccumulator


class AvgAccumulator(Accumulator):
    def __init__(self):
        self.sum_accumulator = SumAccumulator()
        self.count_accumulator = CountAccumulator()

    def accumulate(self, value: Optional[Any]) -> None:
        self.sum_accumulator.accumulate(value)
        self.count_accumulator.accumulate(value)

    @property
    def final_value(self) -> Optional[Any]:
        if (
            self.sum_accumulator.final_value is None
            or self.count_accumulator.final_value is None
        ):
            return None

        return (
            float(self.sum_accumulator.final_value) / self.count_accumulator.final_value
        )
