"""
"""

import pytest
from bitvector import BitVector


@pytest.mark.parametrize("position", list(range(0, 128)))
def test_bitvector_bitwise_and(position: int, BV_0: BitVector, BV_SET: BitVector):

    value = 1 << position

    assert BV_0 & value == 0
    assert value & BV_0 == 0

    assert BV_SET & value == value
    assert value & BV_SET == value


@pytest.mark.parametrize("position", list(range(0, 128)))
def test_bitvector_bitwise_or(position: int, BV_0: BitVector):

    value = 1 << position

    assert BV_0 | value == value
    assert value | BV_0 == value

    test = BitVector(value)

    assert test | value == value
    assert value | test == value


@pytest.mark.parametrize("position", list(range(0, 128)))
def test_bitvector_bitwise_xor(
    position: int, BV_0: BitVector, BV_1: BitVector, BV_SET: BitVector
):

    value = 1 << position

    assert BV_0 ^ value == value
    assert value ^ BV_0 == value

    test = BitVector(value)

    assert test ^ value == 0
    assert value ^ test == 0


def test_bitvector_bitwise_truth_tables(
    BV_0: BitVector, BV_1: BitVector, BV_SET: BitVector
):

    # and
    assert BV_0 & BV_0 == 0
    assert BV_0 & BV_1 == 0
    assert BV_1 & BV_0 == 0
    assert BV_1 & BV_1 == 1

    # or
    assert BV_0 | BV_0 == 0
    assert BV_0 | BV_1 == 1
    assert BV_1 | BV_0 == 1
    assert BV_1 | BV_1 == 1

    # xor
    assert BV_0 ^ BV_0 == 0
    assert BV_0 ^ BV_1 == 1
    assert BV_1 ^ BV_0 == 1
    assert BV_1 ^ BV_1 == 0
