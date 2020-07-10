"""
"""

import pytest

from bitvector import BitVector


@pytest.mark.fast
def test_bitvector_shift_negative(BV_1: BitVector):

    with pytest.raises(ValueError):
        BV_1 << -1

    with pytest.raises(ValueError):
        BV_1 >> -1


@pytest.mark.fast
def test_bitvector_shift_boundries(BV_1: BitVector, BV_HI: BitVector):

    result = BV_1 << 128

    assert result == 0

    result = BV_HI >> 128

    assert result == 0


@pytest.mark.parametrize("position", list(range(0, 128)))
def test_bitvector_shift_left_scalar(position: int, BV_1: BitVector):

    expected = 1 << position
    result = BV_1 << position

    assert result == expected
    assert isinstance(result, BitVector) and result is not BV_1


@pytest.mark.parametrize("position", list(range(0, 128)))
def test_bitvector_shift_left_bitvector(position: int, BV_1: BitVector):

    expected = 1 << position

    with pytest.raises(TypeError):
        # not sure how to get BitVectors to be valid on the RHS of <<
        result = 1 << BitVector(position)
        assert result == expected

    result = BV_1 << BitVector(position)
    assert result == expected


@pytest.mark.parametrize("position", list(range(0, 128)))
def test_bitvector_shift_left_inplace_scalar(position: int, BV_1: BitVector):

    expected = 1 << position
    BV_1 <<= position

    assert BV_1 == expected


@pytest.mark.parametrize("position", list(range(0, 128)))
def test_bitvector_shift_left_inplace_bitvector(position: int, BV_1: BitVector):

    expected = 1 << position

    BV_1 <<= BitVector(position)

    assert BV_1 == expected


@pytest.mark.parametrize("position", list(range(0, 128)))
def test_bitvector_shift_right_scalar(position: int, BV_HI: BitVector):

    expected = (1 << 127) >> position
    result = BV_HI >> position

    assert result == expected
    assert isinstance(result, BitVector) and result is not BV_HI


@pytest.mark.parametrize("position", list(range(0, 128)))
def test_bitvector_shift_right_bitvector(position: int, BV_HI: BitVector):

    expected = (1 << 127) >> position

    with pytest.raises(TypeError):
        # not sure how to get BitVectors to be valid on the RHS of >>
        result = 1 >> BitVector(position)
        assert result == expected

    result = BV_HI >> BitVector(position)
    assert result == expected


@pytest.mark.parametrize("position", list(range(0, 128)))
def test_bitvector_shift_right_inplace_scalar(position: int, BV_HI: BitVector):

    expected = (1 << 127) >> position
    BV_HI >>= position

    assert BV_HI == expected


@pytest.mark.parametrize("position", list(range(0, 128)))
def test_bitvector_shift_right_inplace_bitvector(position: int, BV_HI: BitVector):

    expected = (1 << 127) >> position

    BV_HI >>= BitVector(position)

    assert BV_HI == expected
