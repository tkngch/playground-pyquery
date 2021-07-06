from typing import Any, Optional

from pyarrow import DataType

from pyquery.datatypes import ColumnVector


class LiteralValueVector(ColumnVector):
    """A literal value is repeated for every index in the column."""

    def __init__(self, arrow_type: DataType, value: Optional[Any], size: int):
        self.arrow_type = arrow_type
        self.value = value
        self.size_ = size

    @property
    def data_type(self):
        return self.arrow_type

    def get_value(self, i: int):
        if i < 0 or i >= self.size_:
            raise IndexError
        return self.value

    @property
    def size(self):
        return self.size_
