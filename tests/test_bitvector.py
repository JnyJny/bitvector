"""
"""

import pytest

from bitvector import BitVector, BitField


def intmax(nbits: int) -> int:
    return (1 << nbits) - 1


@pytest.fixture
def ones():
    return BitVector.ones()


@pytest.fixture
def zeros():
    return BitVector.zeros()


@pytest.fixture
def fives():
    return BitVector(int_from_bytes([5] * 16, "big"))


@pytest.fixture
def alphas():
    return BitVector(int_from_bytes([10] * 16, "big"))


def test_bitvector_zeros_classmethod():
    bv = BitVector.zeros()
    assert bv.value == 0


def test_bitvector_ones_classmethod():
    bv = BitVector.ones()
    assert bv.value == bv.MAX


def test_bitvector_create_with_no_args():

    bv = BitVector()
    assert bv
    assert len(bv) == 128
    assert bv.value == 0
    assert bv.MAX == intmax(128)


@pytest.mark.parametrize(
    "given", [0, 1, int.from_bytes([0xA] * 16, "big"), 0xFF00FF00, (1 << 128) - 1],
)
def test_bitvector_create_with_value(given):

    bv = BitVector(given)
    assert bv.value == given


@pytest.mark.parametrize(
    "given, expected", [(0, ValueError), (1, None), (None, TypeError)]
)
def test_bitvector_create_with_size(given, expected):

    if expected:
        with pytest.raises(expected):
            BitVector(size=given)
        return

    bv = BitVector(size=given)
    assert len(bv) == given
    assert bv.MAX == (1 << given) - 1  # maybe too implementation specifc?
