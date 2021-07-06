import csv
from io import StringIO
from typing import Tuple

from pyquery.datatypes.column_vector import ColumnVector
from pyquery.datatypes.schema import Schema


class RecordBatch:
    def __init__(self, schema: Schema, fields: Tuple[ColumnVector, ...]):
        self.schema = schema
        self.fields = fields

    @property
    def row_count(self) -> int:
        return self.fields[0].size

    @property
    def column_count(self) -> int:
        return len(self.fields)

    def field(self, i: int) -> ColumnVector:
        return self.fields[i]

    def to_csv(self) -> str:
        io = StringIO()
        headers = tuple(field.name for field in self.schema.fields)

        writer = csv.DictWriter(io, fieldnames=headers)
        writer.writeheader()
        for row_index in range(self.row_count):
            writer.writerow(
                dict(
                    (header, field.get_value(row_index))
                    for header, field in zip(headers, self.fields)
                )
            )

        return io.getvalue()
