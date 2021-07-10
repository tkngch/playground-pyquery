from typing import Any, Optional

from pyquery.physical_plan.expression.aggregate.accumulator import Accumulator


class CountAccumulator(Accumulator):
    def __init__(self):
        self.value: Optional[int] = None

    def accumulate(self, value: Optional[Any]) -> None:
        if self.value is None:
            self.value = 0
        self.value += 1

    @property
    def final_value(self) -> Optional[int]:
        return self.value
