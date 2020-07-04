"""
"""


import pytest

from bitvector import BitVector
from itertools import permutations


@pytest.mark.parametrize("place", list(range(0, 128)))
def test_bitvector_add_scalar(place: int):

    expected = 1 << place
    test = BitVector()
    assert test == 0

    result = test + expected
    assert isinstance(result, BitVector)
    assert result == expected


@pytest.mark.parametrize("place", list(range(0, 128)))
def test_bitvector_radd_scalar(place: int):

    expected = 1 << place
    test = BitVector()
    assert test == 0

    result = expected + test
    assert isinstance(result, int)
    assert result == expected


@pytest.mark.parametrize("place", list(range(0, 128)))
def test_bitvector_add_bitvector(place: int):

    expected = BitVector(1 << place)
    test = BitVector()
    assert test == 0

    result = test + expected
    assert isinstance(result, BitVector)
    assert result == expected and result is not expected


@pytest.mark.parametrize("place", list(range(0, 128)))
def test_bitvector_iadd_scalar(place: int):

    expected = 1 << place
    test = BitVector()
    assert test == 0

    test += expected
    assert isinstance(test, BitVector)
    assert test == expected


@pytest.mark.parametrize("place", list(range(0, 128)))
def test_bitvector_iadd_bitvector(place: int):

    expected = BitVector(1 << place)
    test = BitVector()
    assert test == 0

    test += expected
    assert isinstance(test, BitVector)
    assert test == expected and test is not expected


@pytest.mark.parametrize("size_a, size_b", list(permutations(range(1, 16), 2)))
def test_bitvector_add_bitvector_mismatched_sizes(size_a, size_b):

    a = BitVector(1, size=size_a)
    b = BitVector(1, size=size_b)

    c = a + b

    assert isinstance(c, BitVector)
    assert len(c) == len(min(a, b, key=len))
    assert c == (2 & c.MAX)
