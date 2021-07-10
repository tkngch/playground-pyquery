from abc import ABC, abstractmethod
from typing import Tuple

from pyquery.datatypes import Schema
from pyquery.physical_plan.physical_plan import PhysicalPlan


class LogicalPlan(ABC):
    @property
    @abstractmethod
    def schema(self) -> Schema:
        raise NotImplementedError

    @property
    @abstractmethod
    def children(self) -> Tuple["LogicalPlan", ...]:
        raise NotImplementedError

    @abstractmethod
    def to_string(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def to_physical_plan(self) -> PhysicalPlan:
        raise NotImplementedError

    def prettify(self) -> str:
        return self._format(indent=0)

    def _format(self, indent: int) -> str:
        formatted = ""
        for i in range(indent):
            formatted += "\t"

        formatted += self.to_string() + "\n"

        for child in self.children:
            formatted += child._format(indent=indent + 1)

        return formatted
