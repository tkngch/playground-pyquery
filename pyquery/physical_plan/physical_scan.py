from functools import cached_property
from typing import Iterable, Tuple

from pyquery.datasource.data_source import DataSource
from pyquery.datatypes import RecordBatch, Schema
from pyquery.physical_plan.physical_plan import PhysicalPlan


class PhysicalScan(PhysicalPlan):
    def __init__(self, data_source: DataSource, projection: Tuple[str, ...]):
        self.data_source = data_source
        self.projection = projection

    @cached_property
    def schema(self) -> Schema:
        return self.data_source.schema.select(self.projection)

    @property
    def children(self) -> Tuple[PhysicalPlan, ...]:
        return ()

    def execute(self) -> Iterable[RecordBatch]:
        return self.data_source.scan(self.projection)

    def to_string(self) -> str:
        return f"Scan: schema={self.schema}, projection=[${', '.join(self.projection)}]"
