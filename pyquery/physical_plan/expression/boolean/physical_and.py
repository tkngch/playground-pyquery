from typing import Any, Optional

from pyarrow import DataType

from pyquery.datatypes import ArrowTypes
from pyquery.physical_plan.expression.boolean.physical_boolean_expression import (
    PhysicalBooleanExpression,
)


class PhysicalAnd(PhysicalBooleanExpression):
    def _compare(
        self, left: Optional[Any], right: Optional[Any], data_type: DataType
    ) -> bool:
        return self._to_bool(left, data_type) and self._to_bool(right, data_type)

    @staticmethod
    def _to_bool(value: Optional[Any], data_type: DataType) -> bool:
        if value is None:
            return False

        if data_type == ArrowTypes.Boolean:
            return bool(value)

        if data_type in (
            ArrowTypes.Int8,
            ArrowTypes.Int16,
            ArrowTypes.Int32,
            ArrowTypes.Int64,
        ):
            return bool(int(value))

        if data_type in (ArrowTypes.Float, ArrowTypes.Double):
            return bool(float(value))

        if data_type == ArrowTypes.String:
            return bool(str(value))

        raise ValueError(
            f"Unsupported data type in comparison expression: ${data_type}"
        )

    def to_string(self) -> str:
        return f"{self.left.to_string()} and {self.right.to_string()}"
