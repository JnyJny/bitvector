"""
"""

import pytest
from itertools import permutations

from bitvector import BitVector


@pytest.mark.fast
@pytest.mark.parametrize("scalar, expected", [(0, True), (1, False)])
def test_bitvector_equal_scalar(scalar, expected):

    b = BitVector()
    assert b == 0

    result = b == scalar
    assert result == expected


@pytest.mark.fast
@pytest.mark.parametrize("scalar, expected", [(0, False), (1, True)])
def test_bitvector_not_equal_scalar(scalar, expected):

    b = BitVector()
    assert b == 0

    result = b != scalar
    assert result == expected


@pytest.mark.parametrize("place", list(range(0, 128)))
def test_bitvector_equal_bitvector(place):
    value = 1 << place
    a = BitVector(value)
    b = BitVector(value)
    assert isinstance(a, BitVector)
    assert isinstance(b, BitVector)
    assert a == b and a is not b


@pytest.mark.parametrize("a, b", list(permutations(range(0, 16), 2)))
def test_bitvector_not_equal_bitvector(a, b):

    assert a != b
    assert BitVector(1 << a) != BitVector(1 << b)


@pytest.mark.parametrize("value", list(range(1, 128)))
def test_bitvector_less_than_scalar(value):

    test = BitVector()
    assert test == 0
    assert test < value


@pytest.mark.parametrize("value", list(range(0, 128)))
def test_bitvector_less_than_or_equal_scalar(value):

    test = BitVector()
    assert test == 0
    assert test <= value


@pytest.mark.parametrize("value", list(range(1, 128)))
def test_bitvector_greater_than_scalar(value):

    test = BitVector(value)
    assert test == value
    assert test > 0


@pytest.mark.parametrize("value", list(range(0, 128)))
def test_bitvector_greater_than_or_equal_scalar(value):

    test = BitVector(value)
    assert test == value
    assert test >= 0


@pytest.mark.parametrize("value", list(range(1, 128)))
def test_bitvector_less_than_bitvector(value):

    test = BitVector()
    bigger = BitVector(value)
    assert test == 0
    assert test < bigger


@pytest.mark.parametrize("value", list(range(0, 128)))
def test_bitvector_less_than_or_equal_bitvector(value):

    test = BitVector()
    bigger = BitVector(value)
    assert test == 0
    assert test <= bigger


@pytest.mark.parametrize("value", list(range(1, 128)))
def test_bitvector_greater_than_bitvector(value):

    test = BitVector(value)
    zero = BitVector()
    assert zero == 0
    assert test == value
    assert test > zero


@pytest.mark.parametrize("value", list(range(0, 128)))
def test_bitvector_greater_than_or_equal_scalar(value):

    test = BitVector(value)
    zero = BitVector()
    assert zero == 0
    assert test == value
    assert test >= zero
