from pathlib import Path
from uuid import uuid4

from pyquery.datasource.csv_data_source import CsvDataSource
from pyquery.logical_plan.expression.aggregate.logical_count import LogicalCount
from pyquery.logical_plan.expression.aggregate.logical_max import LogicalMax
from pyquery.logical_plan.expression.aggregate.logical_min import LogicalMin
from pyquery.logical_plan.expression.col import col
from pyquery.logical_plan.expression.literal.lit import lit
from pyquery.logical_plan.logical_aggregate import LogicalAggregate
from pyquery.logical_plan.logical_projection import LogicalProjection
from pyquery.logical_plan.logical_scan import LogicalScan
from pyquery.logical_plan.logical_selection import LogicalSelection


def test(tmp_path: Path):
    scanned = _scan(tmp_path)
    filtered = LogicalSelection(scanned, col("state").eq(lit("CO")))
    projected = LogicalProjection(
        filtered, (col("id"), col("first_name"), col("last_name"))
    )
    plans = projected.prettify().strip("\n").split("\n")

    assert len(plans) == 3
    assert plans[0] == "Projection: #id, #first_name, #last_name"
    assert plans[1] == "\tSelection: #state = 'CO'"
    assert plans[2] == "\t\tScan: employee; projection=None"


def test_multiplying_and_aliasing(tmp_path: Path):
    scanned = _scan(tmp_path)
    filtered = LogicalSelection(scanned, col("state").eq(lit("CO")))
    projected = LogicalProjection(
        filtered,
        (
            col("id"),
            col("first_name"),
            col("last_name"),
            col("salary"),
            (col("salary").multiply(lit(0.1))).alias("bonus"),
        ),
    )
    final = LogicalSelection(projected, col("bonus").gt(lit(1000)))
    plans = final.prettify().strip("\n").split("\n")

    assert len(plans) == 4
    assert plans[0] == "Selection: #bonus > 1000"
    assert (
        plans[1]
        == "\tProjection: #id, #first_name, #last_name, #salary, #salary * 0.1 as bonus"
    )
    assert plans[2] == "\t\tSelection: #state = 'CO'"
    assert plans[3] == "\t\t\tScan: employee; projection=None"


def test_aggregate_query(tmp_path: Path):
    scanned = _scan(tmp_path)
    aggregated = LogicalAggregate(
        scanned,
        (col("state"),),
        (
            LogicalMin(col("salary")),
            LogicalMax(col("salary")),
            LogicalCount(col("salary")),
        ),
    )
    plans = aggregated.prettify().strip("\n").split("\n")

    assert len(plans) == 2
    assert (
        plans[0]
        == "Aggregate: group-expressions=[#state], aggregate-expressions=[MIN(#salary), MAX(#salary), COUNT(#salary)]"
    )
    assert plans[1] == "\tScan: employee; projection=None"


def _scan(tmp_dir: Path) -> LogicalScan:
    filename = tmp_dir.joinpath(f"data-{str(uuid4())}.csv").as_posix()
    with open(filename, "w") as handler:
        handler.write("id,first_name,last_name,state,job_title,salary\n")
        handler.write("1,Bill,Hopkins,CA,Manager,12000\n")
        handler.write("2,Gregg,Langford,CO,Driver,10000\n")
        handler.write("3,John,Travis,CO,'Manager, Software',11500\n")
        handler.write("4,Von,Mill,,Defensive End,11500\n")

    source = CsvDataSource(filename, schema=None, batch_size=1024)
    return LogicalScan("employee", source, ())
