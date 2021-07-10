from abc import ABC, abstractmethod
from typing import Iterable, Tuple

from pyquery.datatypes.record_batch import RecordBatch
from pyquery.datatypes.schema import Schema


class PhysicalPlan(ABC):
    @property
    @abstractmethod
    def schema(self) -> Schema:
        raise NotImplementedError

    @abstractmethod
    def execute(self) -> Iterable[RecordBatch]:
        raise NotImplementedError

    @property
    @abstractmethod
    def children(self) -> Tuple["PhysicalPlan", ...]:
        raise NotImplementedError

    @abstractmethod
    def to_string(self) -> str:
        raise NotImplementedError
