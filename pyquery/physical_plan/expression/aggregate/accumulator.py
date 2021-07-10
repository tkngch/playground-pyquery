from abc import ABC, abstractmethod
from typing import Any, Optional


class Accumulator(ABC):
    @abstractmethod
    def accumulate(self, value: Optional[Any]) -> None:
        raise NotImplementedError

    @property
    @abstractmethod
    def final_value(self) -> Optional[Any]:
        raise NotImplementedError
