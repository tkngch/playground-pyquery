from typing import Any, Optional

from pyarrow import DataType

from pyquery.physical_plan.expression.boolean.physical_and import PhysicalAnd


class PhysicalOr(PhysicalAnd):
    def _compare(
        self, left: Optional[Any], right: Optional[Any], data_type: DataType
    ) -> bool:
        return self._to_bool(left, data_type) or self._to_bool(right, data_type)

    def to_string(self) -> str:
        return f"{self.left.to_string()} or {self.right.to_string()}"
