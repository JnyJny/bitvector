"""
"""

import pytest
from bitvector import BitVector


def test_bitvector_truthiness(BV_0: BitVector, BV_1: BitVector, BV_SET: BitVector):

    assert bool(BV_0) == False
    assert bool(BV_1) == True

    assert not BV_0 == True
    assert not BV_1 == False

    assert all(BV_0) == False
    assert any(BV_0) == False

    assert all(BV_1) == False
    assert any(BV_1) == True

    assert all(BV_SET) == True
    assert any(BV_SET) == True

    assert 0 in BV_0
    assert 1 not in BV_0

    assert 0 in BV_1
    assert 1 in BV_1

    assert 0 not in BV_SET
    assert 1 in BV_SET

    assert +BV_0 == BV_0
    assert +BV_1 == BV_1
    assert +BV_SET == BV_SET


@pytest.mark.parametrize("value", [1 << p for p in range(0, 128)])
def test_bitvector_bitwise_and(value: int, BV_0: BitVector, BV_SET: BitVector):

    assert BV_0 & value == 0
    assert value & BV_0 == 0

    assert BV_SET & value == value
    assert value & BV_SET == value


@pytest.mark.parametrize("value", [1 << p for p in range(0, 128)])
def test_bitvector_bitwise_iand(value: int, BV_0: BitVector, BV_SET: BitVector):

    BV_0 &= value
    assert BV_0 == 0

    BV_SET &= value
    assert BV_SET == value


@pytest.mark.parametrize("value", [1 << p for p in range(0, 128)])
def test_bitvector_bitwise_or(value: int, BV_0: BitVector):

    assert BV_0 | value == value
    assert value | BV_0 == value

    test = BitVector(value)

    assert test | value == value
    assert value | test == value


@pytest.mark.parametrize("value", [1 << p for p in range(0, 128)])
def test_bitvector_bitwise_ior(value: int, BV_0: BitVector, BV_SET: BitVector):

    BV_0 |= value
    assert BV_0 == value

    BV_SET |= value
    assert BV_SET == (1 << 128) - 1


@pytest.mark.parametrize("value", [1 << p for p in range(0, 128)])
def test_bitvector_bitwise_xor(value: int, BV_0: BitVector):

    assert BV_0 ^ value == value
    assert value ^ BV_0 == value

    test = BitVector(value)

    assert test ^ value == 0
    assert value ^ test == 0


@pytest.mark.parametrize("value", [1 << p for p in range(0, 128)])
def test_bitvector_bitwise_ixor(value: int, BV_0: BitVector):

    BV_0 ^= value
    assert BV_0 == value

    test = BitVector(value)
    test ^= value

    assert test == 0


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


def test_bitvector_bitwise_negation(BV_0: BitVector, BV_SET: BitVector):

    assert ~BV_0 == BV_SET
    assert ~BV_SET == BV_0

    assert -BV_0 == BV_SET
    assert -BV_SET == BV_0
