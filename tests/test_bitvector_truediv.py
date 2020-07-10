"""
"""


import pytest

from bitvector import BitVector
from itertools import permutations


@pytest.mark.parametrize("value", [1 << p for p in range(0, 128)])
def test_bitvector_truediv_scalar(value: int, BV_0: BitVector):

    test = BV_0 / value
    assert test == 0

    test = BitVector(value) / value
    assert test == 1


@pytest.mark.parametrize("value", [1 << p for p in range(0, 128)])
def test_bitvector_rtruediv_scalar(value: int, BV_0: BitVector, BV_1: BitVector):

    result = value / BitVector(value)
    assert isinstance(result, float)
    assert result == 1


@pytest.mark.parametrize("value", [1 << p for p in range(0, 128)])
def test_bitvector_truediv_bitvector(value: int, BV_0: BitVector, BV_1: BitVector):

    test = BitVector(value)

    result = test / BV_1

    assert result == test and result is not test


@pytest.mark.fast
def test_bitvector_itruediv_zeros(BV_0: BitVector, BV_1: BitVector):

    with pytest.raises(ZeroDivisionError):
        1 / BV_0

    with pytest.raises(ZeroDivisionError):
        BV_0 / 0

    with pytest.raises(ZeroDivisionError):
        BV_1 / BV_0

    with pytest.raises(ZeroDivisionError):
        BV_0 /= 0

    with pytest.raises(ZeroDivisionError):
        BV_1 /= BV_0

    BV_0 /= BV_1
    assert BV_0 == 0

    BV_0 /= 1
    assert BV_0 == 0


@pytest.mark.parametrize("value", [1 << p for p in range(0, 128)])
def test_bitvector_itruediv_scalar(value: int, BV_0: BitVector):

    BV_0 /= value
    assert BV_0 == 0

    test = BitVector(value)
    test /= value
    assert test == 1


@pytest.mark.parametrize("value", [1 << p for p in range(0, 128)])
def test_bitvector_itruediv_bitvector(value: int):

    test = BitVector(value)
    test /= value
    assert test == 1


@pytest.mark.parametrize("size_a, size_b", list(permutations(range(1, 16), 2)))
def test_bitvector_truediv_bitvector_mismatched_sizes(size_a, size_b):

    a = BitVector(1, size=size_a)
    b = BitVector(1, size=size_b)

    c = a / b

    assert isinstance(c, BitVector)
    assert len(c) == len(min(a, b, key=len))
    assert c == 1
