from typing import List

from hypothesis import given
from hypothesis.strategies import booleans, floats, integers, lists, text
from pyarrow import array

from pyquery.datatypes import ArrowFieldVector, ArrowTypes, Field, RecordBatch, Schema
from pyquery.physical_plan.expression.boolean.physical_and import PhysicalAnd
from pyquery.physical_plan.expression.boolean.physical_eq import PhysicalEq
from pyquery.physical_plan.expression.boolean.physical_gt import PhysicalGt
from pyquery.physical_plan.expression.boolean.physical_gt_eq import PhysicalGtEq
from pyquery.physical_plan.expression.boolean.physical_lt import PhysicalLt
from pyquery.physical_plan.expression.boolean.physical_lt_eq import PhysicalLtEq
from pyquery.physical_plan.expression.boolean.physical_neq import PhysicalNeq
from pyquery.physical_plan.expression.boolean.physical_or import PhysicalOr
from pyquery.physical_plan.expression.physical_column import PhysicalColumn


@given(lists(integers(min_value=-(2 ** 7), max_value=(2 ** 7 - 1)), min_size=2))
def test_eq_int8(values: List[int]):
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
    expression = PhysicalEq(PhysicalColumn(0), PhysicalColumn(1))
    result = expression.evaluate(batch)

    for i, (a_val, b_val) in enumerate(zip(a, b)):
        assert result.get_value(i) == (a_val == b_val)


@given(lists(integers(min_value=-(2 ** 15), max_value=(2 ** 15 - 1)), min_size=2))
def test_neq_int16(values: List[int]):
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
    expression = PhysicalNeq(PhysicalColumn(0), PhysicalColumn(1))
    result = expression.evaluate(batch)

    for i, (a_val, b_val) in enumerate(zip(a, b)):
        assert result.get_value(i) == (a_val != b_val)


@given(lists(integers(min_value=-(2 ** 31), max_value=(2 ** 31 - 1)), min_size=2))
def test_gteq_int32(values: List[int]):
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
    expression = PhysicalGtEq(PhysicalColumn(0), PhysicalColumn(1))
    result = expression.evaluate(batch)

    for i, (a_val, b_val) in enumerate(zip(a, b)):
        assert result.get_value(i) == (a_val >= b_val)


@given(lists(integers(min_value=-(2 ** 63), max_value=(2 ** 63 - 1)), min_size=2))
def test_lteq_int64(values: List[int]):
    schema = Schema((Field("a", ArrowTypes.Int64), Field("b", ArrowTypes.Int64)))
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
    expression = PhysicalLtEq(PhysicalColumn(0), PhysicalColumn(1))
    result = expression.evaluate(batch)

    for i, (a_val, b_val) in enumerate(zip(a, b)):
        assert result.get_value(i) == (a_val <= b_val)


@given(lists(floats(width=32), min_size=2))
def test_gt_float(values: List[float]):
    schema = Schema((Field("a", ArrowTypes.Float), Field("b", ArrowTypes.Float)))
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
    expression = PhysicalGt(PhysicalColumn(0), PhysicalColumn(1))
    result = expression.evaluate(batch)

    for i, (a_val, b_val) in enumerate(zip(a, b)):
        assert result.get_value(i) == (a_val > b_val)


@given(lists(floats(), min_size=2))
def test_lt_double(values: List[float]):
    schema = Schema((Field("a", ArrowTypes.Double), Field("b", ArrowTypes.Double)))
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
    expression = PhysicalLt(PhysicalColumn(0), PhysicalColumn(1))
    result = expression.evaluate(batch)

    for i, (a_val, b_val) in enumerate(zip(a, b)):
        assert result.get_value(i) == (a_val < b_val)


@given(lists(booleans(), min_size=2))
def test_and_boolean(values: List[bool]):
    schema = Schema((Field("a", ArrowTypes.Boolean), Field("b", ArrowTypes.Boolean)))
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
    expression = PhysicalAnd(PhysicalColumn(0), PhysicalColumn(1))
    result = expression.evaluate(batch)

    for i, (a_val, b_val) in enumerate(zip(a, b)):
        assert result.get_value(i) == (a_val and b_val)


@given(lists(text(), min_size=2))
def test_or_string(values: List[str]):
    schema = Schema((Field("a", ArrowTypes.String), Field("b", ArrowTypes.String)))
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
    expression = PhysicalOr(PhysicalColumn(0), PhysicalColumn(1))
    result = expression.evaluate(batch)

    for i, (a_val, b_val) in enumerate(zip(a, b)):
        assert result.get_value(i) == (bool(a_val) or bool(b_val))
