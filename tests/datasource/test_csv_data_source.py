from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Tuple
from uuid import uuid4

import pytest

from pyquery.datasource.csv_data_source import CsvDataSource


def test_reading_without_projection(tmp_path: Path):
    filename = tmp_path.joinpath(f"data-{str(uuid4())}.csv").as_posix()
    _populate_csv(filename)

    source = CsvDataSource(filename, schema=None, batch_size=1024)
    for result in source.scan(()):
        assert result.row_count == 4
        assert result.column_count == 6

        for i in range(result.column_count):
            assert result.field(i).size == 4


@pytest.mark.parametrize(
    "headers",
    [("first_name", "last_name", "state", "job_title", "salary"), ("id",), ("state",)],
)
def test_reading_with_projection(headers: Tuple[str, ...]):
    with TemporaryDirectory() as tmp_dir:
        filename = Path(tmp_dir).joinpath(f"data-{str(uuid4())}.csv").as_posix()
        _populate_csv(filename)

        source = CsvDataSource(filename, schema=None, batch_size=1024)
        for result in source.scan(headers):
            assert result.row_count == 4
            assert result.column_count == len(headers)

            for i in range(result.column_count):
                assert result.field(i).size == 4


@pytest.mark.parametrize("batch_size", [1, 2, 4])
def test_reading_with_small_batch(batch_size: int):
    with TemporaryDirectory() as tmp_dir:
        filename = Path(tmp_dir).joinpath(f"data-{str(uuid4())}.csv").as_posix()
        _populate_csv(filename)

        source = CsvDataSource(filename, schema=None, batch_size=batch_size)
        for result in source.scan(()):
            assert result.row_count == batch_size
            assert result.column_count == 6

            for i in range(result.column_count):
                assert result.field(i).size == batch_size


def _populate_csv(filename: str) -> None:
    with open(filename, "w") as handler:
        handler.write("id,first_name,last_name,state,job_title,salary\n")
        handler.write("1,Bill,Hopkins,CA,Manager,12000\n")
        handler.write("2,Gregg,Langford,CO,Driver,10000\n")
        handler.write("3,John,Travis,CO,'Manager, Software',11500\n")
        handler.write("4,Von,Mill,,Defensive End,11500\n")
