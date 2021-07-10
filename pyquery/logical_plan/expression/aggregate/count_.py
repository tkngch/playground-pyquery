from pyquery.logical_plan.expression.aggregate.logical_count import LogicalCount
from pyquery.logical_plan.expression.logical_expression import LogicalExpression


def count_(expression: LogicalExpression) -> LogicalCount:
    return LogicalCount(expression)
