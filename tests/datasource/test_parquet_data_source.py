from pathlib import Path
from string import ascii_letters
from tempfile import TemporaryDirectory
from typing import Tuple
from uuid import uuid4

import pyarrow
import pytest
from pyarrow import array, parquet

from pyquery.datasource.parquet_data_source import ParquetDataSource
from pyquery.datatypes import ArrowTypes, Field


def test_reading_schema(tmp_path: Path):
    filename = tmp_path.joinpath(f"data-{str(uuid4())}.parquet").as_posix()
    n_rows = 8
    _populate_parquet(filename, n_rows)

    source = ParquetDataSource(filename, batch_size=1024)

    schema = source.schema
    assert len(schema.fields) == 9
    assert schema.fields[0] == Field(name="id", data_type=ArrowTypes.Int32)
    assert schema.fields[1] == Field(name="bool_col", data_type=ArrowTypes.Boolean)
    assert schema.fields[2] == Field(name="tinyint_col", data_type=ArrowTypes.Int8)
    assert schema.fields[3] == Field(name="smallint_col", data_type=ArrowTypes.Int16)
    assert schema.fields[4] == Field(name="int_col", data_type=ArrowTypes.Int32)
    assert schema.fields[5] == Field(name="bigint_col", data_type=ArrowTypes.Int64)
    assert schema.fields[6] == Field(name="float_col", data_type=ArrowTypes.Float)
    assert schema.fields[7] == Field(name="double_col", data_type=ArrowTypes.Double)
    assert schema.fields[8] == Field(name="string_col", data_type=ArrowTypes.String)


def test_reading_without_projection(tmp_path: Path):
    filename = tmp_path.joinpath(f"data-{str(uuid4())}.parquet").as_posix()
    n_rows = 8
    _populate_parquet(filename, n_rows)

    source = ParquetDataSource(filename, batch_size=1024)
    for result in source.scan(()):
        assert result.row_count == n_rows
        assert result.column_count == 9

        for i in range(result.column_count):
            assert result.field(i).size == n_rows


@pytest.mark.parametrize(
    "headers",
    [
        ("bool_col", "tinyint_col", "int_col", "bigint_col", "double_col"),
        ("id",),
        ("float_col",),
        ("string_col",),
    ],
)
def test_reading_with_projection(headers: Tuple[str, ...]):
    with TemporaryDirectory() as tmp_dir:
        filename = Path(tmp_dir).joinpath(f"data-{str(uuid4())}.parquet").as_posix()
        n_rows = 8
        _populate_parquet(filename, n_rows)

        source = ParquetDataSource(filename, batch_size=1024)
        for result in source.scan(headers):
            assert result.row_count == n_rows
            assert result.column_count == len(headers)

            for i in range(result.column_count):
                assert result.field(i).size == n_rows


@pytest.mark.parametrize("batch_size", [1, 2, 4, 8])
def test_reading_with_small_batch(batch_size: int):
    headers = (
        "bool_col",
        "tinyint_col",
        "smallint_col",
        "int_col",
        "bigint_col",
        "float_col",
        "double_col",
        "string_col",
    )
    with TemporaryDirectory() as tmp_dir:
        filename = Path(tmp_dir).joinpath(f"data-{str(uuid4())}.parquet").as_posix()
        n_rows = 8
        _populate_parquet(filename, n_rows)

        source = ParquetDataSource(filename, batch_size=batch_size)
        for result in source.scan(headers):
            assert result.row_count == batch_size
            assert result.column_count == len(headers)

            for i in range(result.column_count):
                assert result.field(i).size == batch_size


def _populate_parquet(filename: str, n_rows: int) -> None:
    table = pyarrow.Table.from_pydict(
        {
            "id": array(list(range(n_rows)), ArrowTypes.Int32),
            "bool_col": array([i % 2 == 0 for i in range(n_rows)], ArrowTypes.Boolean),
            "tinyint_col": array(list(range(n_rows)), ArrowTypes.Int8),
            "smallint_col": array(list(range(n_rows)), ArrowTypes.Int16),
            "int_col": array(list(range(n_rows)), ArrowTypes.Int32),
            "bigint_col": array(list(range(n_rows)), ArrowTypes.Int64),
            "float_col": array([i * 1.1 for i in range(n_rows)], ArrowTypes.Float),
            "double_col": array([i * 1.2 for i in range(n_rows)], ArrowTypes.Double),
            "string_col": array(
                [ascii_letters[i] for i in range(n_rows)], ArrowTypes.String
            ),
        }
    )
    parquet.write_table(table, filename)
