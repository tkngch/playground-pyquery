from abc import ABC, abstractmethod
from typing import Any, Optional

from pyarrow import DataType, array

from pyquery.datatypes import ArrowFieldVector, ColumnVector
from pyquery.physical_plan.expression.physical_binary_expression import (
    PhysicalBinaryExpression,
)


class PhysicalBooleanExpression(PhysicalBinaryExpression, ABC):
    def _evaluate(self, left: ColumnVector, right: ColumnVector) -> ColumnVector:
        results = tuple(
            self._compare(left.get_value(i), right.get_value(i), left.data_type)
            for i in range(left.size)
        )
        return ArrowFieldVector(array(results))

    @abstractmethod
    def _compare(
        self, left: Optional[Any], right: Optional[Any], data_type: DataType
    ) -> bool:
        raise NotImplementedError
