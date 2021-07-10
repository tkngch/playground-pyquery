from pathlib import Path
from string import ascii_letters
from tempfile import TemporaryDirectory
from uuid import uuid4

from hypothesis import given
from hypothesis.strategies import integers
from pyarrow import Table, array, parquet

from pyquery.execution_context import ExecutionContext
from pyquery.logical_plan.expression.aggregate.count_ import count_
from pyquery.logical_plan.expression.aggregate.max_ import max_
from pyquery.logical_plan.expression.aggregate.min_ import min_
from pyquery.logical_plan.expression.aggregate.sum_ import sum_
from pyquery.logical_plan.expression.col import col
from pyquery.logical_plan.expression.col_index import col_index
from pyquery.logical_plan.expression.literal.lit import lit


@given(integers(min_value=1, max_value=64))
def test(batch_size: int):
    with TemporaryDirectory() as tmp_dir:
        filepath = Path(tmp_dir).joinpath(f"data-{str(uuid4())}.parquet").as_posix()
        _populate_parquet_file(filepath)

        dataframe = (
            ExecutionContext(batch_size=batch_size)
            .parquet(filepath)
            .filter(col("string0").eq(lit("a")))
            .filter(col("string1").eq(lit("a")).or_(col("string1").eq(lit("c"))))
            .aggregate(
                (col("string1"),),
                (
                    count_(col("string0")),
                    sum_(col("int0")),
                    min_(col("float1")),
                    max_(col("float2")),
                ),
            )
            .project(
                (
                    col("string1"),
                    col_index(1).alias("count_string0"),
                    col_index(2).alias("sum_int0"),
                    col_index(3).alias("min_float1"),
                    col_index(4).alias("max_float2"),
                )
            )
        )
        batch = list(dataframe.execute())[0]
    rows = batch.to_csv().strip("\r\n").split("\r\n")

    assert len(rows) == 3
    assert rows[0] == "string1,count_string0,sum_int0,min_float1,max_float2"
    assert rows[1] == "a,11,330,0.1,60.2"
    assert rows[2] == "c,11,352,2.1,62.2"


def _populate_parquet_file(filepath: str) -> None:
    n_rows = 64
    table = Table.from_pydict(
        {
            "id": array(list(range(n_rows))),
            "string0": array([ascii_letters[i % 2] for i in range(n_rows)]),
            "string1": array([ascii_letters[i % 3] for i in range(n_rows)]),
            "int0": array([int(i) for i in range(n_rows)]),
            "float1": array([float(i + 0.1) for i in range(n_rows)]),
            "float2": array([float(i + 0.2) for i in range(n_rows)]),
        }
    )
    parquet.write_table(table, filepath)
