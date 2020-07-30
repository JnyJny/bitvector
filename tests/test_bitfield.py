"""
"""

import pytest

from bitvector import BitVector, BitField, ReadOnlyBitField
from itertools import combinations


def test_bitfield_create_no_args():

    with pytest.raises(TypeError):
        BitField()


@pytest.mark.parametrize("offset", list(range(0, 128)))
def test_bitfield_create_with_offset(offset: int):

    test = BitField(offset)

    assert isinstance(test, BitField)
    assert isinstance(test.field, slice)
    assert (offset, offset + 1, 1) == test.field.indices(128)


@pytest.mark.parametrize("offset,width", list(combinations(range(1, 16), 2)))
def test_bitfield_create_with_offset_and_width(offset: int, width: int):

    test = BitField(offset, width)

    assert (offset, min(16, offset + width), 1) == test.field.indices(16)


def test_bitfield_in_bitvector_subclass_get_values(SixteenBitClass: type):

    test = SixteenBitClass(0xABCD)

    assert test == 0xABCD

    assert test.byte0 == 0xCD
    assert test.byte1 == 0xAB

    # 0xD
    assert test.bit0 == 1
    assert test.bit1 == 0
    assert test.bit2 == 1
    assert test.bit3 == 1

    # 0xC
    assert test.bit4 == 0
    assert test.bit5 == 0
    assert test.bit6 == 1
    assert test.bit7 == 1

    # 0xB
    assert test.bit8 == 1
    assert test.bit9 == 1
    assert test.bitA == 0
    assert test.bitB == 1

    # 0xA
    assert test.bitC == 0
    assert test.bitD == 1
    assert test.bitE == 0
    assert test.bitF == 1


def test_bitfield_in_bitvector_subclass_get_values(SixteenBitClass: type):

    test = SixteenBitClass(0x0000)

    assert test == 0

    test.byte0 = 0x55
    test.byte1 = 0xAA

    assert test.byte0 == 0x55
    assert test.byte1 == 0xAA

    # 0x5
    assert test.bit0 == 1
    assert test.bit1 == 0
    assert test.bit2 == 1
    assert test.bit3 == 0

    # 0x5
    assert test.bit4 == 1
    assert test.bit5 == 0
    assert test.bit6 == 1
    assert test.bit7 == 0

    # 0xA
    assert test.bit8 == 0
    assert test.bit9 == 1
    assert test.bitA == 0
    assert test.bitB == 1

    # 0xA
    assert test.bitC == 0
    assert test.bitD == 1
    assert test.bitE == 0
    assert test.bitF == 1


def test_readonly_bitfield_in_bitvector_subclass():
    class TestClass(BitVector):
        def __init__(self):
            super().__init__(value=0xDEADBEEF, size=32)

        dead = BitField(16, 16)
        beef = ReadOnlyBitField(0, 16)

    test = TestClass()

    assert test.dead == 0xDEAD
    assert test.beef == 0xBEEF

    test.dead = 0xcafe

    assert test.dead == 0xcafe

    with pytest.raises(TypeError):
        test.beef = 0x0bad

    assert test.beef == 0xbeef
