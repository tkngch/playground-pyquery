from pathlib import Path
from uuid import uuid4

from pyquery.data_frame import DataFrame
from pyquery.datasource.csv_data_source import CsvDataSource
from pyquery.logical_plan.expression.aggregate.logical_count import LogicalCount
from pyquery.logical_plan.expression.aggregate.logical_max import LogicalMax
from pyquery.logical_plan.expression.aggregate.logical_min import LogicalMin
from pyquery.logical_plan.expression.col import col
from pyquery.logical_plan.expression.literal.lit import lit
from pyquery.logical_plan.logical_plan import LogicalPlan
from pyquery.logical_plan.logical_scan import LogicalScan
from pyquery.logical_plan.optimiser.rule.projection_push_down_rule import (
    ProjectionPushDownRule,
)


def test(tmp_path: Path):
    dataframe = _read_csv(tmp_path).project((col("first_name"), col("last_name")))
    rule = ProjectionPushDownRule()
    optimised = rule.optimise(dataframe.logical_plan)

    optimised_plans = _list_plan_strings(optimised)
    assert len(optimised_plans) == 2
    assert optimised_plans[0] == "Projection: #first_name, #last_name"
    assert optimised_plans[1] == "\tScan: employee; [first_name, last_name]"

    original_plans = _list_plan_strings(dataframe.logical_plan)
    assert optimised_plans[0] == original_plans[0]
    assert optimised_plans[1] != original_plans[1]


def test_with_selection(tmp_path: Path):
    dataframe = (
        _read_csv(tmp_path)
        .filter(col("state").eq(lit("CO")))
        .project((col("id"), col("first_name"), col("last_name")))
    )
    rule = ProjectionPushDownRule()
    optimised = rule.optimise(dataframe.logical_plan)

    optimised_plans = _list_plan_strings(optimised)
    assert len(optimised_plans) == 3
    assert optimised_plans[0] == "Projection: #id, #first_name, #last_name"
    assert optimised_plans[1] == "\tSelection: #state = 'CO'"
    assert (
        optimised_plans[2] == "\t\tScan: employee; [first_name, id, last_name, state]"
    )

    original_plans = _list_plan_strings(dataframe.logical_plan)
    assert optimised_plans[0] == original_plans[0]
    assert optimised_plans[1] == original_plans[1]
    assert optimised_plans[2] != original_plans[2]


def test_with_selection_and_aggregation(tmp_path: Path):
    dataframe = (
        _read_csv(tmp_path)
        .filter(col("state").eq(lit("CO")).or_(col("state").eq(lit("CA"))))
        .aggregate(
            (col("state"),),
            (
                LogicalMin(col("salary")),
                LogicalMax(col("salary")),
                LogicalCount(col("salary")),
            ),
        )
    )
    rule = ProjectionPushDownRule()
    optimised = rule.optimise(dataframe.logical_plan)

    optimised_plans = _list_plan_strings(optimised)
    assert len(optimised_plans) == 3
    assert (
        optimised_plans[0]
        == "Aggregate: group-expressions=[#state], aggregate-expressions=[MIN(#salary), MAX(#salary), COUNT(#salary)]"
    )
    assert optimised_plans[1] == "\tSelection: #state = 'CO' OR #state = 'CA'"
    assert optimised_plans[2] == "\t\tScan: employee; [salary, state]"

    original_plans = _list_plan_strings(dataframe.logical_plan)
    assert optimised_plans[0] == original_plans[0]
    assert optimised_plans[1] == original_plans[1]
    assert optimised_plans[2] != original_plans[2]


def _read_csv(tmp_dir: Path) -> DataFrame:
    filename = tmp_dir.joinpath(f"data-{str(uuid4())}.csv").as_posix()
    with open(filename, "w") as handler:
        handler.write("id,first_name,last_name,state,job_title,salary\n")
        handler.write("1,Bill,Hopkins,CA,Manager,12000\n")
        handler.write("2,Gregg,Langford,CO,Driver,10000\n")
        handler.write("3,John,Travis,CO,'Manager, Software',11500\n")
        handler.write("4,Von,Mill,,Defensive End,11500\n")

    source = CsvDataSource(filename, schema=None, batch_size=1024)
    scan = LogicalScan("employee", source, ())
    return DataFrame(scan)


def _list_plan_strings(plan: LogicalPlan):
    return plan.prettify().strip("\n").split("\n")
