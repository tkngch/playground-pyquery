from pyquery.logical_plan.expression.logical_column import LogicalColumn


def col(name: str) -> LogicalColumn:
    return LogicalColumn(name)
