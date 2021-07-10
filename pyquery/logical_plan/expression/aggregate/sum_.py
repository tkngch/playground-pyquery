from pyquery.logical_plan.expression.aggregate.logical_sum import LogicalSum
from pyquery.logical_plan.expression.logical_expression import LogicalExpression


def sum_(expression: LogicalExpression) -> LogicalSum:
    return LogicalSum(expression)
