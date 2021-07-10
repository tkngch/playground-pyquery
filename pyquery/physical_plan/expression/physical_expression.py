from abc import ABC, abstractmethod

from pyquery.datatypes.column_vector import ColumnVector
from pyquery.datatypes.record_batch import RecordBatch


class PhysicalExpression(ABC):
    @abstractmethod
    def evaluate(self, data: RecordBatch) -> ColumnVector:
        raise NotImplementedError

    @abstractmethod
    def to_string(self) -> str:
        raise NotImplementedError
