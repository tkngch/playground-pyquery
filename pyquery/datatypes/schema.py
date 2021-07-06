from dataclasses import dataclass
from typing import List, Tuple

import pyarrow

from pyquery.datatypes.field import Field


@dataclass
class Schema:
    fields: Tuple[Field, ...]

    @staticmethod
    def from_arrow(arrow_schema: pyarrow.Schema) -> "Schema":
        fields: List[Field] = []

        for name in arrow_schema.names:
            fields.append(Field(name=name, data_type=arrow_schema.field(name).type))

        return Schema(tuple(fields))

    def to_arrow(self) -> pyarrow.Schema:
        arrow_schema = pyarrow.Schema()
        for field in self.fields:
            arrow_schema.append(field.to_arrow())

        return arrow_schema

    def project(self, indices: Tuple[int, ...]) -> "Schema":
        return Schema(tuple(self.fields[index] for index in indices))

    def select(self, names: Tuple[str, ...]) -> "Schema":
        field_by_name = dict((field.name, field) for field in self.fields)
        return Schema(tuple(field_by_name[name] for name in names))
