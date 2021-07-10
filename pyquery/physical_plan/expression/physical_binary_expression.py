from abc import ABC, abstractmethod

from pyquery.datatypes.column_vector import ColumnVector
from pyquery.datatypes.record_batch import RecordBatch
from pyquery.physical_plan.expression.physical_expression import PhysicalExpression


class PhysicalBinaryExpression(PhysicalExpression, ABC):
    def __init__(self, left: PhysicalExpression, right: PhysicalExpression):
        self.left = left
        self.right = right

    def evaluate(self, data: RecordBatch) -> ColumnVector:
        left_evaluated = self.left.evaluate(data)
        right_evaluated = self.right.evaluate(data)

        assert left_evaluated.size == right_evaluated.size
        if left_evaluated.data_type != right_evaluated.data_type:
            raise RuntimeError(
                "Binary expression operands do not have the same type: "
                f"{left_evaluated.data_type} != {right_evaluated.data_type}"
            )

        return self._evaluate(left_evaluated, right_evaluated)

    @abstractmethod
    def _evaluate(self, left: ColumnVector, right: ColumnVector) -> ColumnVector:
        raise NotImplementedError
