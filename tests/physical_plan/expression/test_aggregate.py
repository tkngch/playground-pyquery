from math import isfinite
from typing import List

from hypothesis import given
from hypothesis.strategies import floats, integers, lists, text
from pytest import approx

from pyquery.physical_plan.expression.aggregate.physical_avg import PhysicalAvg
from pyquery.physical_plan.expression.aggregate.physical_count import PhysicalCount
from pyquery.physical_plan.expression.aggregate.physical_max import PhysicalMax
from pyquery.physical_plan.expression.aggregate.physical_min import PhysicalMin
from pyquery.physical_plan.expression.aggregate.physical_sum import PhysicalSum
from pyquery.physical_plan.expression.physical_column import PhysicalColumn


@given(lists(integers(min_value=-(2 ** 7), max_value=(2 ** 7 - 1))))
def test_max_int8(values: List[int]):
    expression = PhysicalMax(PhysicalColumn(0))
    accumulator = expression.create_accumulator()
    for value in values:
        accumulator.accumulate(value)

    if values:
        assert accumulator.final_value == max(values)
    else:
        assert accumulator.final_value is None


@given(lists(integers(min_value=-(2 ** 7), max_value=(2 ** 7 - 1))))
def test_min_int8(values: List[int]):
    expression = PhysicalMin(PhysicalColumn(0))
    accumulator = expression.create_accumulator()
    for value in values:
        accumulator.accumulate(value)

    if values:
        assert accumulator.final_value == min(values)
    else:
        assert accumulator.final_value is None


@given(lists(floats(allow_infinity=False)))
def test_sum_double(values_: List[float]):
    values = tuple(x if isfinite(x) else None for x in values_)

    expression = PhysicalSum(PhysicalColumn(0))
    accumulator = expression.create_accumulator()
    for value in values:
        accumulator.accumulate(value)

    non_nulls = tuple(x for x in values if x is not None)
    if non_nulls:
        assert accumulator.final_value == sum(non_nulls)
    else:
        assert accumulator.final_value is None


@given(lists(integers(min_value=-(2 ** 15), max_value=(2 ** 15 - 1))))
def test_avg_int16(values: List[int]):
    expression = PhysicalAvg(PhysicalColumn(0))
    accumulator = expression.create_accumulator()
    for value in values:
        accumulator.accumulate(value)

    if values:
        assert accumulator.final_value == approx(sum(values) / len(values))
    else:
        assert accumulator.final_value is None


@given(lists(text()))
def test_count_string(values: List[str]):
    expression = PhysicalCount(PhysicalColumn(0))
    accumulator = expression.create_accumulator()
    for value in values:
        accumulator.accumulate(value)

    if values:
        assert accumulator.final_value == len(values)
    else:
        assert accumulator.final_value is None
