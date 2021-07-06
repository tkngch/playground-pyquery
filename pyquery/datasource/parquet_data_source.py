from functools import cached_property
from typing import Iterable, Tuple

from pyarrow.parquet import ParquetFile

from pyquery.datasource.data_source import DataSource
from pyquery.datatypes import ArrowFieldVector, RecordBatch, Schema


class ParquetDataSource(DataSource):
    def __init__(self, filename: str, batch_size: int) -> None:
        self.filename = filename
        self.batch_size = batch_size

    @cached_property
    def schema(self) -> Schema:
        file = ParquetFile(self.filename)
        return Schema.from_arrow(file.schema_arrow)

    def scan(self, projection: Tuple[str, ...]) -> Iterable[RecordBatch]:
        read_schema = self.schema if not projection else self.schema.select(projection)
        field_names = tuple(field.name for field in read_schema.fields)

        file = ParquetFile(self.filename)
        for batch in file.iter_batches(
            batch_size=self.batch_size, columns=list(field_names)
        ):
            fields = tuple(ArrowFieldVector(batch.column(name)) for name in field_names)
            yield RecordBatch(read_schema, fields)
