from pyquery.datatypes.arrow_types import ArrowTypes
from pyquery.datatypes.column_vector import ColumnVector
from pyquery.datatypes.literal_value_vector import LiteralValueVector
from pyquery.datatypes.record_batch import RecordBatch
from pyquery.physical_plan.expression.physical_expression import PhysicalExpression


class PhysicalLiteralDouble(PhysicalExpression):
    def __init__(self, value: float):
        self.value = value

    def evaluate(self, data: RecordBatch) -> ColumnVector:
        return LiteralValueVector(ArrowTypes.Double, self.value, data.row_count)

    def to_string(self) -> str:
        return str(self.value)
