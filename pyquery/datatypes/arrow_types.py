from dataclasses import dataclass
from typing import ClassVar

import pyarrow as pa
from pyarrow import DataType


@dataclass
class ArrowTypes:
    Boolean: ClassVar[DataType] = pa.bool_()
    Int8: ClassVar[DataType] = pa.int8()
    Int16: ClassVar[DataType] = pa.int16()
    Int32: ClassVar[DataType] = pa.int32()
    Int64: ClassVar[DataType] = pa.int64()
    Float: ClassVar[DataType] = pa.float32()
    Double: ClassVar[DataType] = pa.float64()
    String: ClassVar[DataType] = pa.string()
