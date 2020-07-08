"""
"""


import pytest

from bitvector import BitVector
from itertools import permutations


@pytest.mark.parametrize("value", [1 << p for p in range(0, 128)])
def test_bitvector_add_scalar(value: int, BV_0: BitVector, BV_1: BitVector):

    result = BV_0 + value
    assert isinstance(result, BitVector)
    assert result == value

    result = BV_1 + value
    assert isinstance(result, BitVector)
    assert result == value + 1


@pytest.mark.parametrize("value", [1 << p for p in range(0, 128)])
def test_bitvector_radd_scalar(value: int, BV_0: BitVector, BV_1: BitVector):

    result = value + BV_0
    assert isinstance(result, int)
    assert result == value

    result = value + BV_1
    assert isinstance(result, int)
    assert result == value + 1


@pytest.mark.parametrize("value", [1 << p for p in range(0, 128)])
def test_bitvector_add_bitvector(value: int, BV_0: BitVector, BV_1: BitVector):

    expected = BitVector(value)

    result = BV_0 + expected
    assert isinstance(result, BitVector)
    assert result == expected and result is not expected

    result = BV_1 + expected
    assert isinstance(result, BitVector)
    assert result == expected.value + 1


@pytest.mark.parametrize("value", [1 << p for p in range(0, 128)])
def test_bitvector_iadd_scalar(value: int, BV_0: BitVector, BV_1: BitVector):

    BV_0 += value
    assert BV_0 == value

    BV_1 += value
    assert BV_1 == value + 1


@pytest.mark.parametrize("value", [1 << p for p in range(0, 128)])
def test_bitvector_iadd_bitvector(value: int, BV_0: BitVector, BV_1: BitVector):

    bv = BitVector(value)

    BV_0 += bv
    assert BV_0 == value

    BV_1 += bv
    assert BV_1 == value + 1


@pytest.mark.parametrize("size_a, size_b", list(permutations(range(1, 16), 2)))
def test_bitvector_add_bitvector_mismatched_sizes(size_a, size_b):

    a = BitVector(1, size=size_a)
    b = BitVector(1, size=size_b)

    c = a + b

    assert isinstance(c, BitVector)
    assert len(c) == len(min(a, b, key=len))
    assert c == (2 & c.MAX)
