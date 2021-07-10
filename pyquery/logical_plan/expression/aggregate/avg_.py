from pyquery.logical_plan.expression.aggregate.logical_avg import LogicalAvg
from pyquery.logical_plan.expression.logical_expression import LogicalExpression


def avg_(expression: LogicalExpression) -> LogicalAvg:
    return LogicalAvg(expression)
