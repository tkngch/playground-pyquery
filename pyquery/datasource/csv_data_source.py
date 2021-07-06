import csv
from functools import cache, cached_property
from typing import Any, Dict, Iterable, List, Optional, Tuple

import pyarrow

from pyquery.datasource.data_source import DataSource
from pyquery.datatypes import ArrowFieldVector, ArrowTypes, Field, RecordBatch, Schema

_Record = Tuple[Any, ...]


class CsvDataSource(DataSource):
    def __init__(
        self,
        filename: str,
        schema: Optional[Schema],
        batch_size: int,
    ) -> None:
        self.filename = filename
        self.schema_ = schema
        self._batch_size = batch_size

    @cached_property
    def schema(self) -> Schema:
        if self.schema_:
            return self.schema_
        return self._infer_schema()

    @cache
    def _infer_schema(self) -> Schema:
        with open(self.filename, "r") as handler:
            reader = csv.reader(handler)
            headers = next(reader)

        return Schema(tuple(Field(header, ArrowTypes.String) for header in headers))

    def scan(self, projection: Tuple[str, ...]) -> Iterable[RecordBatch]:
        read_schema = self.schema if not projection else self.schema.select(projection)

        with open(self.filename, "r") as handler:
            reader = csv.DictReader(handler)

            records = self._make_empty_records(read_schema)
            for row in reader:
                for field in read_schema.fields:
                    records[field.name].append(row[field.name])

                if len(records[read_schema.fields[0].name]) == self._batch_size:
                    yield self._create_batch(read_schema, records)
                    records = self._make_empty_records(read_schema)

            if records[read_schema.fields[0].name]:
                yield self._create_batch(read_schema, records)

    @staticmethod
    def _make_empty_records(schema: Schema) -> Dict[str, List[Any]]:
        return dict((field.name, []) for field in schema.fields)

    @staticmethod
    def _create_batch(schema: Schema, records: Dict[str, List[Any]]) -> RecordBatch:
        fields = tuple(
            ArrowFieldVector(pyarrow.array(records[field.name], type=field.data_type))
            for field in schema.fields
        )
        return RecordBatch(schema, fields)
