from pyquery.logical_plan.expression.aggregate.logical_min import LogicalMin
from pyquery.logical_plan.expression.logical_expression import LogicalExpression


def min_(expression: LogicalExpression) -> LogicalMin:
    return LogicalMin(expression)
