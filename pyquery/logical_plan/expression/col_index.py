from pyquery.logical_plan.expression.logical_column_index import LogicalColumnIndex


def col_index(i: int) -> LogicalColumnIndex:
    return LogicalColumnIndex(i)
