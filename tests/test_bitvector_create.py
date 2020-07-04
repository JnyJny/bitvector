"""
"""

import pytest

from bitvector import BitVector, BitField


ONES_128 = (1 << 128) - 1


def test_bitvector_zeros_classmethod():
    bv = BitVector.zeros()
    assert bv.value == 0
    assert bv.MAX == ONES_128


def test_bitvector_ones_classmethod():
    bv = BitVector.ones()
    assert bv.value == bv.MAX
    assert bv.MAX == ONES_128


def test_bitvector_create_with_no_args():

    bv = BitVector()
    assert bv
    assert len(bv) == 128
    assert bv.value == 0
    assert bv.MAX == ONES_128


@pytest.mark.parametrize("given", [1 << b for b in range(0, 128)])
def test_bitvector_create_with_value(given):

    bv = BitVector(given)
    assert bv.value == given


@pytest.mark.parametrize(
    "given, expected",
    [(-1, ValueError), (0, ValueError), (1, None), (None, TypeError)],
)
def test_bitvector_create_with_size(given, expected):

    if expected:
        with pytest.raises(expected):
            BitVector(size=given)
        return

    bv = BitVector(size=given)
    assert len(bv) == given


@pytest.mark.parametrize("size", list(range(1, 1024)))
def test_bitvector_create_with_range_of_sizes(size):

    b = BitVector(size=size)
    assert b
    assert b.value == 0
    assert b.MAX == (1 << size) - 1
