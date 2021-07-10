from typing import Any, Dict, Iterable, List, Optional, Tuple

from pyarrow import array

from pyquery.datatypes import ArrowFieldVector, RecordBatch, Schema
from pyquery.physical_plan.expression.aggregate.accumulator import Accumulator
from pyquery.physical_plan.expression.aggregate.physical_aggregate_expression import (
    PhysicalAggregateExpression,
)
from pyquery.physical_plan.expression.physical_expression import PhysicalExpression
from pyquery.physical_plan.physical_plan import PhysicalPlan


class PhysicalHashAggregate(PhysicalPlan):
    def __init__(
        self,
        plan: PhysicalPlan,
        group_expressions: Tuple[PhysicalExpression, ...],
        aggregate_expressions: Tuple[PhysicalAggregateExpression, ...],
        schema: Schema,
    ):
        self.plan = plan
        self.group_expressions = group_expressions
        self.aggregate_expressions = aggregate_expressions
        self.schema_ = schema

    @property
    def schema(self) -> Schema:
        return self.schema_

    @property
    def children(self) -> Tuple[PhysicalPlan, ...]:
        return (self.plan,)

    def to_string(self) -> str:
        group_expressions = ", ".join(
            [expression.to_string() for expression in self.group_expressions]
        )
        agg_expressions = ", ".join(
            [expression.to_string() for expression in self.aggregate_expressions]
        )
        return f"Aggregate: group-expressions=[{group_expressions}], aggregate-expressions=[{agg_expressions}]"

    def execute(self) -> Iterable[RecordBatch]:
        hash_map = self._process_batches()

        field_vectors: List[List[Any]] = [[] for _ in range(len(self.schema_.fields))]
        for group_key, accumulators in hash_map.items():
            for i, key in enumerate(group_key):
                field_vectors[i].append(key)
            for i, accumulator in enumerate(accumulators):
                field_vectors[i + len(group_key)].append(accumulator.final_value)

        fields = tuple(
            ArrowFieldVector(array(vector, type=field.data_type))
            for vector, field in zip(field_vectors, self.schema_.fields)
        )
        yield RecordBatch(self.schema, fields)

    def _process_batches(
        self,
    ) -> Dict[Tuple[Optional[Any], ...], Tuple[Accumulator, ...]]:
        result: Dict[Tuple[Optional[Any], ...], Tuple[Accumulator, ...]] = {}

        for batch in self.plan.execute():
            group_keys = tuple(
                expression.evaluate(batch) for expression in self.group_expressions
            )
            input_values = tuple(
                expression.expression.evaluate(batch)
                for expression in self.aggregate_expressions
            )

            for row_index in range(batch.row_count):
                row_key = tuple(key.get_value(row_index) for key in group_keys)
                if row_key not in result:
                    result.update(
                        {
                            row_key: tuple(
                                expression.create_accumulator()
                                for expression in self.aggregate_expressions
                            )
                        }
                    )

                for i in range(len(self.aggregate_expressions)):
                    result[row_key][i].accumulate(input_values[i].get_value(row_index))

        return result
