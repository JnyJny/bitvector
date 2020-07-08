"""
"""


import pytest

from bitvector import BitVector
from itertools import permutations


@pytest.mark.parametrize("value", [1 << p for p in range(0, 128)])
def test_bitvector_mul_scalar(value: int, BV_0: BitVector, BV_1: BitVector):

    assert BV_0 * value == 0
    assert BV_1 * value == value


@pytest.mark.parametrize("value", [1 << p for p in range(0, 128)])
def test_bitvector_rmul_scalar(value: int, BV_0: BitVector, BV_1: BitVector):

    result = value * BV_0
    assert isinstance(result, int)
    assert result == 0

    result = value * BV_1
    assert isinstance(result, int)
    assert result == value


@pytest.mark.parametrize("value", [1 << p for p in range(0, 128)])
def test_bitvector_mul_bitvector(value: int, BV_0: BitVector, BV_1: BitVector):

    expected = BitVector(value)

    result = BV_1 * expected
    assert isinstance(result, BitVector)
    assert result == expected and result is not expected

    result = BV_0 * expected
    assert isinstance(result, BitVector)
    assert result == 0


@pytest.mark.parametrize("value", [1 << p for p in range(0, 128)])
def test_bitvector_imul_scalar(value: int, BV_0: BitVector, BV_1: BitVector):

    BV_0 *= value
    assert BV_0 == 0

    BV_1 *= value
    assert BV_1 == value and BV_1 is not value


@pytest.mark.parametrize("value", [1 << p for p in range(0, 128)])
def test_bitvector_imul_bitvector(value: int, BV_0: BitVector, BV_1: BitVector):

    test = BitVector(value)

    BV_0 *= test
    assert BV_0 == 0

    BV_1 *= test
    assert BV_1 == test and BV_1 is not test


@pytest.mark.parametrize("size_a, size_b", list(permutations(range(1, 16), 2)))
def test_bitvector_mul_bitvector_mismatched_sizes(size_a, size_b):

    a = BitVector(1, size=size_a)
    b = BitVector(1, size=size_b)

    c = a * b

    assert isinstance(c, BitVector)
    assert len(c) == len(min(a, b, key=len))
    assert c == 1 and c == a and c == b
