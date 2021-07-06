from dataclasses import dataclass

import pyarrow
from pyarrow import DataType


@dataclass
class Field:
    name: str
    data_type: DataType

    def to_arrow(self) -> pyarrow.Field:
        return pyarrow.Field().with_name(self.name).with_type(self.data_type)
