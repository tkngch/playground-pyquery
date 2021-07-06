from functools import cached_property
from typing import Any, Optional

from pyarrow import (
    Array,
    BooleanArray,
    DataType,
    Int8Array,
    Int16Array,
    Int32Array,
    Int64Array,
    StringArray,
)
from pyarrow.lib import DoubleArray, FloatArray

from pyquery.datatypes.arrow_types import ArrowTypes
from pyquery.datatypes.column_vector import ColumnVector


class ArrowFieldVector(ColumnVector):
    def __init__(self, field: Array) -> None:
        self.field = field

    @cached_property
    def data_type(self) -> Optional[DataType]:
        if isinstance(self.field, BooleanArray):
            return ArrowTypes.Boolean
        if isinstance(self.field, DoubleArray):
            return ArrowTypes.Double
        if isinstance(self.field, FloatArray):
            return ArrowTypes.Float
        if isinstance(self.field, Int8Array):
            return ArrowTypes.Int8
        if isinstance(self.field, Int16Array):
            return ArrowTypes.Int16
        if isinstance(self.field, Int32Array):
            return ArrowTypes.Int32
        if isinstance(self.field, Int64Array):
            return ArrowTypes.Int64
        if isinstance(self.field, StringArray):
            return ArrowTypes.String

        raise ValueError(f"Type '{type(self.field)}' is not supported.")

    def get_value(self, i: int) -> Optional[Any]:
        return self.field.take([i]).tolist()[0]

    @cached_property
    def size(self) -> int:
        return len(self.field.tolist())
