"""
"""


import pytest

from bitvector import BitVector
from itertools import permutations


@pytest.mark.parametrize("place", list(range(0, 128)))
def test_bitvector_sub_scalar(place: int):

    expected = 1 << place
    test = BitVector(expected)
    assert test == expected and test is not expected

    result = test - expected
    assert isinstance(result, BitVector)
    assert result == 0


@pytest.mark.parametrize("place", list(range(0, 128)))
def test_bitvector_rsub_scalar(place: int):

    expected = 1 << place
    test = BitVector(expected)
    assert test == expected and test is not expected

    result = expected - test
    assert isinstance(result, int)
    assert result == 0


@pytest.mark.parametrize("place", list(range(0, 128)))
def test_bitvector_sub_bitvector(place: int):

    expected = BitVector(1 << place)
    test = BitVector(1 << place)
    assert test == expected and test is not expected

    result = test - expected
    assert isinstance(result, BitVector)
    assert result == 0


@pytest.mark.parametrize("place", list(range(0, 128)))
def test_bitvector_isub_scalar(place: int):

    expected = 1 << place
    test = BitVector(expected)
    assert test == expected and test is not expected

    test -= expected
    assert isinstance(test, BitVector)
    assert test == 0


@pytest.mark.parametrize("place", list(range(0, 128)))
def test_bitvector_isub_bitvector(place: int):

    expected = BitVector(1 << place)
    test = BitVector(1 << place)
    assert test == expected and test is not expected

    test -= expected
    assert isinstance(test, BitVector)
    assert test == 0


@pytest.mark.parametrize("size_a, size_b", list(permutations(range(1, 16), 2)))
def test_bitvector_sub_bitvector_mismatched_sizes(size_a, size_b):

    a = BitVector(1, size=size_a)
    b = BitVector(1, size=size_b)

    c = a - b

    assert isinstance(c, BitVector)
    assert len(c) == len(min(a, b, key=len))
    assert c == 0
