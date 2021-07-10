from typing import Any, Optional

from pyquery.physical_plan.expression.aggregate.accumulator import Accumulator


class SumAccumulator(Accumulator):
    def __init__(self):
        self.value: Optional[Any] = None

    def accumulate(self, value: Optional[Any]) -> None:
        if self.value is None:
            self.value = value

        elif isinstance(value, int):
            self.value += int(value)
        elif isinstance(value, float):
            self.value += float(value)

        elif value is not None:
            raise ValueError(f"SUM is not implemented for data type: {type(value)}")

    @property
    def final_value(self) -> Optional[Any]:
        return self.value
