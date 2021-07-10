from math import isfinite
from typing import List

from hypothesis import given
from hypothesis.strategies import floats, integers, lists
from pyarrow import array
from pytest import approx

from pyquery.datatypes import ArrowFieldVector, ArrowTypes, Field, RecordBatch, Schema
from pyquery.physical_plan.expression.math.physical_add import PhysicalAdd
from pyquery.physical_plan.expression.math.physical_divide import PhysicalDivide
from pyquery.physical_plan.expression.math.physical_modulus import PhysicalModulus
from pyquery.physical_plan.expression.math.physical_multiply import PhysicalMultiply
from pyquery.physical_plan.expression.math.physical_subtract import PhysicalSubtract
from pyquery.physical_plan.expression.physical_column import PhysicalColumn


@given(lists(integers(min_value=-(2 ** 7), max_value=(2 ** 7 - 1)), min_size=2))
def test_add_int8(values: List[int]):
    schema = Schema((Field("a", ArrowTypes.Int8), Field("b", ArrowTypes.Int8)))
    n_entries = len(values) // 2
    a = values[:n_entries]
    b = values[n_entries : (2 * n_entries)]

    batch = RecordBatch(
        schema,
        (
            ArrowFieldVector(array(a, type=schema.fields[0].data_type)),
            ArrowFieldVector(array(b, type=schema.fields[1].data_type)),
        ),
    )
    expression = PhysicalAdd(PhysicalColumn(0), PhysicalColumn(1))
    result = expression.evaluate(batch)

    for i, (a_val, b_val) in enumerate(zip(a, b)):
        assert result.get_value(i) == (a_val + b_val)


@given(lists(integers(min_value=-(2 ** 15), max_value=(2 ** 15 - 1)), min_size=2))
def test_subtract_int16(values: List[int]):
    schema = Schema((Field("a", ArrowTypes.Int16), Field("b", ArrowTypes.Int16)))
    n_entries = len(values) // 2
    a = values[:n_entries]
    b = values[n_entries : (2 * n_entries)]

    batch = RecordBatch(
        schema,
        (
            ArrowFieldVector(array(a, type=schema.fields[0].data_type)),
            ArrowFieldVector(array(b, type=schema.fields[1].data_type)),
        ),
    )
    expression = PhysicalSubtract(PhysicalColumn(0), PhysicalColumn(1))
    result = expression.evaluate(batch)

    for i, (a_val, b_val) in enumerate(zip(a, b)):
        assert result.get_value(i) == (a_val - b_val)


@given(lists(integers(min_value=1, max_value=(2 ** 31 - 1)), min_size=2))
def test_modulus_int32(values: List[int]):
    schema = Schema((Field("a", ArrowTypes.Int32), Field("b", ArrowTypes.Int32)))
    n_entries = len(values) // 2
    a = values[:n_entries]
    b = values[n_entries : (2 * n_entries)]

    batch = RecordBatch(
        schema,
        (
            ArrowFieldVector(array(a, type=schema.fields[0].data_type)),
            ArrowFieldVector(array(b, type=schema.fields[1].data_type)),
        ),
    )
    expression = PhysicalModulus(PhysicalColumn(0), PhysicalColumn(1))
    result = expression.evaluate(batch)

    for i, (a_val, b_val) in enumerate(zip(a, b)):
        assert result.get_value(i) == (a_val % b_val)


@given(lists(floats(width=32, allow_infinity=False), min_size=2))
def test_divide_float(values: List[float]):
    schema = Schema((Field("a", ArrowTypes.Float), Field("b", ArrowTypes.Float)))
    n_entries = len(values) // 2
    a = tuple(x if isfinite(x) else None for x in values[:n_entries])
    b = tuple(x if isfinite(x) else None for x in values[n_entries : (2 * n_entries)])

    batch = RecordBatch(
        schema,
        (
            ArrowFieldVector(array(a, type=schema.fields[0].data_type)),
            ArrowFieldVector(array(b, type=schema.fields[1].data_type)),
        ),
    )
    expression = PhysicalDivide(PhysicalColumn(0), PhysicalColumn(1))
    result = expression.evaluate(batch)

    for i, (a_val, b_val) in enumerate(zip(a, b)):
        if a_val is None or b_val is None or abs(b_val) < 1e-16:
            assert result.get_value(i) is None
        else:
            assert result.get_value(i) == approx(a_val / b_val)


@given(lists(floats(allow_infinity=False), min_size=2))
def test_multiply_double(values: List[float]):
    schema = Schema((Field("a", ArrowTypes.Double), Field("b", ArrowTypes.Double)))
    n_entries = len(values) // 2
    a = tuple(x if isfinite(x) else None for x in values[:n_entries])
    b = tuple(x if isfinite(x) else None for x in values[n_entries : (2 * n_entries)])

    batch = RecordBatch(
        schema,
        (
            ArrowFieldVector(array(a, type=schema.fields[0].data_type)),
            ArrowFieldVector(array(b, type=schema.fields[1].data_type)),
        ),
    )
    expression = PhysicalMultiply(PhysicalColumn(0), PhysicalColumn(1))
    result = expression.evaluate(batch)

    for i, (a_val, b_val) in enumerate(zip(a, b)):
        if a_val is None or b_val is None:
            assert result.get_value(i) is None
        else:
            assert result.get_value(i) == approx(a_val * b_val)
