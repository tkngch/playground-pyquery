from pyquery.logical_plan.expression.aggregate.logical_max import LogicalMax
from pyquery.logical_plan.expression.logical_expression import LogicalExpression


def max_(expression: LogicalExpression) -> LogicalMax:
    return LogicalMax(expression)
