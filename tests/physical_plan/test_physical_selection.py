from pathlib import Path
from string import ascii_letters
from uuid import uuid4

from pyarrow import Table, array, parquet

from pyquery.datasource.data_source import DataSource
from pyquery.datasource.parquet_data_source import ParquetDataSource
from pyquery.physical_plan.expression.boolean.physical_eq import PhysicalEq
from pyquery.physical_plan.expression.literal.physical_literal_string import (
    PhysicalLiteralString,
)
from pyquery.physical_plan.expression.physical_column import PhysicalColumn
from pyquery.physical_plan.physical_scan import PhysicalScan
from pyquery.physical_plan.physical_selection import PhysicalSelection


def test(tmp_path: Path):
    scan = PhysicalScan(_get_data_source(tmp_path), ())

    filtering_column = 1
    filtering_value = "a"
    filtering_expression = PhysicalEq(
        PhysicalColumn(filtering_column), PhysicalLiteralString(filtering_value)
    )

    selection = PhysicalSelection(scan, filtering_expression)

    for batch in selection.execute():
        assert batch.column_count == 6
        assert batch.row_count == 4
        assert all(
            batch.field(filtering_column).get_value(i) == filtering_value
            for i in range(batch.row_count)
        )


def _get_data_source(tmp_dir: Path) -> DataSource:
    n_rows = 8
    table = Table.from_pydict(
        {
            "id": array(list(range(n_rows))),
            "string0": array([ascii_letters[i % 2] for i in range(n_rows)]),
            "string1": array([ascii_letters[i % 3] for i in range(n_rows)]),
            "float0": array([1.1 * (i + 1) for i in range(n_rows)]),
            "float1": array([1.2 * (i + 1) for i in range(n_rows)]),
            "float2": array([1.3 * (i + 1) for i in range(n_rows)]),
        }
    )

    filename = tmp_dir.joinpath(f"data-{str(uuid4())}.parquet").as_posix()
    parquet.write_table(table, filename)

    return ParquetDataSource(filename, batch_size=1024)
