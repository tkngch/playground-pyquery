from typing import Iterable, Tuple

from pyarrow import array

from pyquery.datatypes import (
    ArrowFieldVector,
    ArrowTypes,
    ColumnVector,
    RecordBatch,
    Schema,
)
from pyquery.physical_plan.expression.physical_expression import PhysicalExpression
from pyquery.physical_plan.physical_plan import PhysicalPlan


class PhysicalSelection(PhysicalPlan):
    def __init__(self, plan: PhysicalPlan, expression: PhysicalExpression):
        self.plan = plan
        self.expression = expression

    @property
    def schema(self) -> Schema:
        return self.plan.schema

    @property
    def children(self) -> Tuple[PhysicalPlan, ...]:
        return (self.plan,)

    def execute(self) -> Iterable[RecordBatch]:
        for batch in self.plan.execute():
            if batch.fields[0].size == 0:
                continue
            evaluation = self.expression.evaluate(batch)
            assert isinstance(evaluation, ArrowFieldVector)

            filtered_fields = tuple(
                self._filter(batch.field(i), evaluation)
                for i in range(len(batch.schema.fields))
            )

            yield RecordBatch(self.schema, filtered_fields)

    @staticmethod
    def _filter(column: ColumnVector, selection: ArrowFieldVector) -> ArrowFieldVector:
        assert selection.data_type == ArrowTypes.Boolean
        values = tuple(
            column.get_value(i) for i in range(column.size) if selection.get_value(i)
        )
        return ArrowFieldVector(array(values))

    def to_string(self) -> str:
        return f"Selection: {self.expression.to_string()}"
