from abc import ABC, abstractmethod
from typing import Any, Optional

from pyarrow import DataType


class ColumnVector(ABC):
    @property
    @abstractmethod
    def data_type(self) -> DataType:
        raise NotImplementedError

    @abstractmethod
    def get_value(self, i: int) -> Optional[Any]:
        raise NotImplementedError

    @property
    @abstractmethod
    def size(self) -> int:
        raise NotImplementedError
