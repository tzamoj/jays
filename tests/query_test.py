import pytest

import operator

import jays.utils

from .query import boolean, filters, flatten, select, slices, advanced


@pytest.mark.parametrize("case", boolean.cases.values(), ids=boolean.cases.keys())
def test_boolean(case):
    assert jays.utils.compare(case.query(case.data), case.expected, operator.eq)


@pytest.mark.parametrize("case", filters.cases.values(), ids=filters.cases.keys())
def test_filters(case):
    assert jays.utils.compare(case.query(case.data), case.expected, operator.eq)


@pytest.mark.parametrize("case", flatten.cases.values(), ids=flatten.cases.keys())
def test_flatten(case):
    assert jays.utils.compare(case.query(case.data), case.expected, operator.eq)


@pytest.mark.parametrize("case", select.cases.values(), ids=select.cases.keys())
def test_select(case):
    assert jays.utils.compare(case.query(case.data), case.expected, operator.eq)


@pytest.mark.parametrize("case", slices.cases.values(), ids=slices.cases.keys())
def test_slices(case):
    assert jays.utils.compare(case.query(case.data), case.expected, operator.eq)



@pytest.mark.parametrize("case", advanced.cases.values(), ids=advanced.cases.keys())
def test_advanced(case):
    assert jays.utils.compare(case.query(case.data), case.expected, operator.eq)
