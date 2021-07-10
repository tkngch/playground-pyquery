from abc import ABC, abstractmethod

from pyquery.datatypes import Field
from pyquery.logical_plan.expression.logical_expression import LogicalExpression
from pyquery.logical_plan.logical_plan import LogicalPlan
from pyquery.physical_plan.expression.aggregate.physical_aggregate_expression import (
    PhysicalAggregateExpression,
)


class LogicalAggregateExpression(ABC):
    def __init__(self, name: str, expression: LogicalExpression) -> None:
        self.name = name
        self.expression = expression

    def to_field(self, plan: LogicalPlan) -> Field:
        return self.expression.to_field(plan)

    def to_string(self) -> str:
        return f"{self.name}({self.expression.to_string()})"

    @abstractmethod
    def to_physical_expression(self, plan: LogicalPlan) -> PhysicalAggregateExpression:
        raise NotImplementedError
