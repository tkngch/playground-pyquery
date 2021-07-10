from functools import cached_property
from typing import Tuple

from pyquery.datasource.data_source import DataSource
from pyquery.datatypes import Schema
from pyquery.logical_plan.logical_plan import LogicalPlan
from pyquery.physical_plan.physical_plan import PhysicalPlan
from pyquery.physical_plan.physical_scan import PhysicalScan


class LogicalScan(LogicalPlan):
    """Plan to fetch data from a datasource with an optional projection."""

    def __init__(self, path: str, data_source: DataSource, projection: Tuple[str, ...]):
        self.path = path
        self.data_source = data_source
        self.projection = projection

    @cached_property
    def schema(self) -> Schema:
        if not self.projection:
            return self.data_source.schema
        return self.data_source.schema.select(self.projection)

    @property
    def children(self) -> Tuple[LogicalPlan, ...]:
        return ()

    def to_string(self) -> str:
        if not self.projection:
            return f"Scan: {self.path}; projection=None"
        return f"Scan: {self.path}; [{', '.join(self.projection)}]"

    def to_physical_plan(self) -> PhysicalPlan:
        return PhysicalScan(data_source=self.data_source, projection=self.projection)
