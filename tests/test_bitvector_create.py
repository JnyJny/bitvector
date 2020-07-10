"""
"""

import pytest

from bitvector import BitVector, BitField


@pytest.mark.fast
def test_bitvector_zeros_classmethod():
    bv = BitVector.zeros()
    assert bv.value == 0
    assert len(bv) == 128


@pytest.mark.fast
def test_bitvector_ones_classmethod():
    bv = BitVector.ones()
    assert bv.value == 0xFFFF_FFFF_FFFF_FFFF_FFFF_FFFF_FFFF_FFFF
    assert len(bv) == 128


@pytest.mark.fast
def test_bitvector_create_with_no_args():

    bv = BitVector()
    assert isinstance(bv, BitVector)
    assert len(bv) == 128
    assert bv.value == 0
    assert bv.MAX == 0xFFFF_FFFF_FFFF_FFFF_FFFF_FFFF_FFFF_FFFF


@pytest.mark.parametrize("given", [1 << b for b in range(0, 128)])
def test_bitvector_create_with_value(given):

    bv = BitVector(given)
    assert bv.value == given


@pytest.mark.fast
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
    assert isinstance(b, BitVector)
    assert b.value == 0
    assert len(b) == size
