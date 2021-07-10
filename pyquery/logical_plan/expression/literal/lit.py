from typing import Any

from pyquery.logical_plan.expression.literal.logical_literal_double import (
    LogicalLiteralDouble,
)
from pyquery.logical_plan.expression.literal.logical_literal_long import (
    LogicalLiteralLong,
)
from pyquery.logical_plan.expression.literal.logical_literal_string import (
    LogicalLiteralString,
)
from pyquery.logical_plan.expression.logical_expression import LogicalExpression


def lit(value: Any) -> LogicalExpression:
    if isinstance(value, str):
        return LogicalLiteralString(value)
    if isinstance(value, int):
        return LogicalLiteralLong(value)
    if isinstance(value, float):
        return LogicalLiteralDouble(value)

    raise ValueError(f"Unsupported type: '{type(value)}'.")
