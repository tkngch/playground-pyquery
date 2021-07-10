from pathlib import Path
from string import ascii_letters
from uuid import uuid4

from pyarrow import Table, array, parquet
from pytest import approx

from pyquery.datasource.data_source import DataSource
from pyquery.datasource.parquet_data_source import ParquetDataSource
from pyquery.datatypes import ArrowTypes, Field, Schema
from pyquery.physical_plan.expression.aggregate.physical_max import PhysicalMax
from pyquery.physical_plan.expression.aggregate.physical_min import PhysicalMin
from pyquery.physical_plan.expression.aggregate.physical_sum import PhysicalSum
from pyquery.physical_plan.expression.physical_column import PhysicalColumn
from pyquery.physical_plan.physical_hash_aggregate import PhysicalHashAggregate
from pyquery.physical_plan.physical_scan import PhysicalScan


def test(tmp_path: Path):
    scan = PhysicalScan(_get_data_source(tmp_path), ())

    groups = (PhysicalColumn(1), PhysicalColumn(2))
    aggregates = (
        PhysicalMax(PhysicalColumn(3)),
        PhysicalMin(PhysicalColumn(4)),
        PhysicalSum(PhysicalColumn(5)),
    )
    schema = Schema(
        (
            Field(name="group0", data_type=ArrowTypes.String),
            Field(name="group1", data_type=ArrowTypes.String),
            Field(name="aggregate0", data_type=ArrowTypes.Int8),
            Field(name="aggregate1", data_type=ArrowTypes.Double),
            Field(name="aggregate2", data_type=ArrowTypes.Double),
        )
    )

    agg = PhysicalHashAggregate(scan, groups, aggregates, schema)

    for batch in agg.execute():
        assert batch.column_count == len(groups) + len(aggregates)
        assert batch.row_count == 4

        group0 = tuple(batch.field(0).get_value(i) for i in range(batch.row_count))
        assert group0 == ("a", "b", "a", "b")

        group1 = tuple(batch.field(1).get_value(i) for i in range(batch.row_count))
        assert group1 == ("a", "b", "c", "d")

        aggregate0 = tuple(batch.field(2).get_value(i) for i in range(batch.row_count))
        assert aggregate0 == (13, 14, 15, 16)

        aggregate1 = tuple(batch.field(3).get_value(i) for i in range(batch.row_count))
        assert aggregate1 == approx((1.2, 2.4, 3.6, 4.8))

        aggregate2 = tuple(batch.field(4).get_value(i) for i in range(batch.row_count))
        assert aggregate2 == approx((36.4, 41.6, 46.8, 52.0))


def _get_data_source(tmp_dir: Path) -> DataSource:
    n_rows = 16
    table = Table.from_pydict(
        {
            "id": array(list(range(n_rows))),
            "string0": array([ascii_letters[i % 2] for i in range(n_rows)]),
            "string1": array([ascii_letters[i % 4] for i in range(n_rows)]),
            "int0": array([int(i + 1) for i in range(n_rows)]),
            "float1": array([1.2 * (i + 1) for i in range(n_rows)]),
            "float2": array([1.3 * (i + 1) for i in range(n_rows)]),
        }
    )

    filename = tmp_dir.joinpath(f"data-{str(uuid4())}.parquet").as_posix()
    parquet.write_table(table, filename)

    return ParquetDataSource(filename, batch_size=1024)
