from typing import Iterable, Tuple

from pyquery.datatypes.record_batch import RecordBatch
from pyquery.datatypes.schema import Schema
from pyquery.physical_plan.expression.physical_expression import PhysicalExpression
from pyquery.physical_plan.physical_plan import PhysicalPlan


class PhysicalProjection(PhysicalPlan):
    def __init__(
        self,
        plan: PhysicalPlan,
        schema: Schema,
        expressions: Tuple[PhysicalExpression, ...],
    ):
        self.plan = plan
        self.schema_ = schema
        self.expressions = expressions

    @property
    def schema(self) -> Schema:
        return self.schema_

    @property
    def children(self) -> Tuple[PhysicalPlan, ...]:
        return (self.plan,)

    def execute(self) -> Iterable[RecordBatch]:
        for batch in self.plan.execute():
            columns = tuple(
                expression.evaluate(batch) for expression in self.expressions
            )
            yield RecordBatch(self.schema_, columns)

    def to_string(self) -> str:
        return f"Projection: [{', '.join([expr.to_string() for expr in self.expressions])}]"
