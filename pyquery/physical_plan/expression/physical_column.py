from pyquery.datatypes.column_vector import ColumnVector
from pyquery.datatypes.record_batch import RecordBatch
from pyquery.physical_plan.expression.physical_expression import PhysicalExpression


class PhysicalColumn(PhysicalExpression):
    def __init__(self, i: int):
        self.i = i

    def evaluate(self, data: RecordBatch) -> ColumnVector:
        return data.field(self.i)

    def to_string(self) -> str:
        return f"#{self.i}"
