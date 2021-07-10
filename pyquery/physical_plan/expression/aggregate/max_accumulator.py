from typing import Any, Optional

from pyquery.physical_plan.expression.aggregate.accumulator import Accumulator


class MaxAccumulator(Accumulator):
    def __init__(self):
        self.value: Optional[Any] = None

    def accumulate(self, value: Optional[Any]) -> None:
        if self._is_max(value):
            self.value = value

    def _is_max(self, value: Optional[Any]) -> bool:
        if self.value is None:
            return True
        if value is None:
            return False

        if isinstance(value, int):
            return int(value) > int(self.value)
        if isinstance(value, float):
            return float(value) > float(self.value)
        if isinstance(value, str):
            return str(value) > str(self.value)

        raise ValueError(f"MAX is not implemented for data type: {type(value)}")

    @property
    def final_value(self) -> Optional[Any]:
        return self.value
