from abc import ABC, abstractmethod
from functools import cached_property
from typing import Iterable, Tuple

from pyquery.datatypes import RecordBatch, Schema


class DataSource(ABC):
    @cached_property
    @abstractmethod
    def schema(self) -> Schema:
        raise NotImplementedError

    @abstractmethod
    def scan(self, projection: Tuple[str, ...]) -> Iterable[RecordBatch]:
        raise NotImplementedError
