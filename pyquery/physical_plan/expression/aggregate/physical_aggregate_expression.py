from abc import ABC, abstractmethod

from pyquery.physical_plan.expression.aggregate.accumulator import Accumulator
from pyquery.physical_plan.expression.physical_expression import PhysicalExpression


class PhysicalAggregateExpression(ABC):
    def __init__(self, expression: PhysicalExpression):
        self.expression = expression

    @abstractmethod
    def create_accumulator(self) -> Accumulator:
        raise NotImplementedError

    @abstractmethod
    def to_string(self) -> str:
        raise NotImplementedError
