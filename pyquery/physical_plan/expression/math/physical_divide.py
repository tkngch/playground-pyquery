from typing import Any, Optional

from pyarrow import DataType

from pyquery.datatypes.arrow_types import ArrowTypes
from pyquery.physical_plan.expression.math.physical_math_expression import (
    PhysicalMathExpression,
)


class PhysicalDivide(PhysicalMathExpression):
    def _calculate(
        self, left: Optional[Any], right: Optional[Any], data_type: DataType
    ) -> Optional[Any]:
        if left is None or right is None:
            return None

        if data_type in (
            ArrowTypes.Int8,
            ArrowTypes.Int16,
            ArrowTypes.Int32,
            ArrowTypes.Int64,
        ):
            if int(right) == 0:
                return None
            return int(left) // int(right)

        if data_type in (ArrowTypes.Float, ArrowTypes.Double):
            if abs(right) < 1e-16:
                return None
            return float(left) / float(right)

        raise ValueError(f"Unsupported data type in math expression: ${data_type}")

    def to_string(self) -> str:
        return f"{self.left.to_string()} / {self.right.to_string()}"
