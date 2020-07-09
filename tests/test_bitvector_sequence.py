"""
"""

import pytest

from bitvector import BitVector
from itertools import combinations


@pytest.mark.parametrize("position", list(range(0, 128)))
def test_bitvector_get_single_bit(position: int, BV_0: BitVector, BV_SET: BitVector):

    assert BV_0[position] == 0
    assert BV_SET[position] == 1


@pytest.mark.parametrize("start,stop", list(combinations(range(0, 128), 2)))
def test_bitvector_get_slice(start: int, stop: int, BV_0: BitVector, BV_SET: BitVector):

    assert BV_0[start:stop] == 0
    assert BV_SET[start:stop] != 0


@pytest.mark.parametrize("position", list(range(0, 128)))
def test_bitvector_set_single_bit(position: int, BV_0: BitVector, BV_SET: BitVector):

    BV_0[position] = 1
    BV_SET[position] = 0

    assert BV_0[position] == 1
    assert BV_SET[position] == 0


@pytest.mark.parametrize("start,stop", list(combinations(range(0, 128), 2)))
def test_bitvector_set_slice(start: int, stop: int, BV_0: BitVector, BV_SET: BitVector):

    BV_0[start:stop] = 1
    BV_SET[start:stop] = 0

    assert BV_0[start:stop] == 1
    assert BV_SET[start:stop] == 0


@pytest.mark.parametrize("skip", [1, 2, 4, 8, 16, 32, 64, 128])
def test_bitvector_get_slice_with_skip(skip: int, BV_SET: BitVector):

    value = BV_SET[::skip]
    expected = len(BV_SET) / skip
    assert value.bit_length() == expected and value != 0


@pytest.mark.parametrize(
    "skip, expected",
    [
        (1, 0xFFFF_FFFF_FFFF_FFFF_FFFF_FFFF_FFFF_FFFF),
        (2, 0x5555_5555_5555_5555_5555_5555_5555_5555),
        (3, 0x4924_9249_2492_4924_9249_2492_4924_9249),
        (4, 0x1111_1111_1111_1111_1111_1111_1111_1111),
        (5, 0x3119_5311_9531_1953_1195_3119_5311_9531),
        (5, 0x2108_4210_8421_0842_1084_2108_4210_8421),
        (6, 0x4104_1041_0410_4104_1041_0410_4104_1041),
        (7, 0x4081_0204_0810_2040_8102_0408_1020_4081),
        (8, 0x0101_0101_0101_0101_0101_0101_0101_0101),
    ],
)
def test_bitvector_set_slice_with_skip(skip, expected, BV_0: BitVector):

    BV_0[::skip] = 0xFFFF_FFFF_FFFF_FFFF_FFFF_FFFF_FFFF_FFFF
