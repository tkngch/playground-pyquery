from typing import Any, Optional

from pyarrow import DataType

from pyquery.datatypes.arrow_types import ArrowTypes
from pyquery.physical_plan.expression.boolean.physical_boolean_expression import (
    PhysicalBooleanExpression,
)


class PhysicalNeq(PhysicalBooleanExpression):
    def _compare(
        self, left: Optional[Any], right: Optional[Any], data_type: DataType
    ) -> bool:
        if left is None or right is None:
            return False

        if data_type in (
            ArrowTypes.Int8,
            ArrowTypes.Int16,
            ArrowTypes.Int32,
            ArrowTypes.Int64,
        ):
            return int(left) != int(right)

        if data_type in (ArrowTypes.Float, ArrowTypes.Double):
            return float(left) != float(right)

        if data_type == ArrowTypes.String:
            return str(left) != str(right)

        raise ValueError(
            f"Unsupported data type in comparison expression: ${data_type}"
        )

    def to_string(self) -> str:
        return f"{self.left.to_string()} != {self.right.to_string()}"
