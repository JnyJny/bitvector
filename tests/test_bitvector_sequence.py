"""
"""

import pytest

from bitvector import BitVector
from itertools import combinations


@pytest.mark.fast
@pytest.mark.parametrize("position", list(range(0, 128)))
def test_bitvector_get_single_bit(position: int, BV_0: BitVector, BV_SET: BitVector):

    assert BV_0[position] == 0
    assert BV_SET[position] == 1


@pytest.mark.slow
@pytest.mark.parametrize("start,stop", list(combinations(range(0, 128), 2)))
def test_bitvector_get_slice(start: int, stop: int, BV_0: BitVector, BV_SET: BitVector):

    assert BV_0[start:stop] == 0
    assert BV_SET[start:stop] != 0


@pytest.mark.fast
@pytest.mark.parametrize("position", list(range(0, 128)))
def test_bitvector_set_single_bit(position: int, BV_0: BitVector, BV_SET: BitVector):

    BV_0[position] = 1
    BV_SET[position] = 0

    assert BV_0[position] == 1
    assert BV_SET[position] == 0


@pytest.mark.slow
@pytest.mark.parametrize("start,stop", list(combinations(range(0, 128), 2)))
def test_bitvector_set_slice(start: int, stop: int, BV_0: BitVector, BV_SET: BitVector):

    BV_0[start:stop] = 1
    BV_SET[start:stop] = 0

    assert BV_0[start:stop] == 1
    assert BV_SET[start:stop] == 0


@pytest.mark.fast
@pytest.mark.parametrize("skip", [1, 2, 4, 8, 16, 32, 64, 128])
def test_bitvector_get_slice_with_skip(skip: int, BV_SET: BitVector):

    value = BV_SET[::skip]
    expected = len(BV_SET) / skip
    assert value.bit_length() == expected and value != 0


@pytest.mark.fast
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


@pytest.mark.fast
def test_bitvector_reverse():

    given = BitVector(0xAAAA_AAAA_AAAA_AAAA_AAAA_AAAA_AAAA_AAAA)

    result = given[::-1]

    assert result == 0x5555_5555_5555_5555_5555_5555_5555_5555


@pytest.mark.parametrize("neg_ndx, pos_ndx", zip(range(-128, 0), range(0, 128)))
def test_bitvector_negative_index(neg_ndx: int, pos_ndx, BV_SET: BitVector):

    assert BV_SET[pos_ndx] == 1
    assert BV_SET[neg_ndx] == 1

    BV_SET[neg_ndx] = 0
    assert BV_SET[pos_ndx] == 0


@pytest.mark.fast
def test_bitvector_access_out_of_bounds(BV_0: BitVector):

    oob = len(BV_0) + 1

    with pytest.raises(IndexError):
        BV_0[oob]

    with pytest.raises(IndexError):
        BV_0[oob] = 1


@pytest.mark.fast
def test_bitvector_set_slice_with_bool(BV_SET: BitVector):

    assert BV_SET[0:4] == 0xF

    BV_SET[0:4] = False

    assert BV_SET[0:4] == 0

    BV_SET[0:4] = True

    assert BV_SET[0:4] == 0xF


@pytest.mark.fast
@pytest.mark.parametrize("key", ["key", None, 0.0])
def test_bitvector_get_with_invalid_key(key: object, BV_0: BitVector):

    with pytest.raises(ValueError):
        BV_0[key]


@pytest.mark.fast
@pytest.mark.parametrize("key", ["key", None, 0.0])
def test_bitvector_set_with_invalid_key(key: object, BV_0: BitVector):

    with pytest.raises(ValueError):
        BV_0[key] = 1
