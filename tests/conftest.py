"""
"""

import pytest

from bitvector import BitVector, BitField


@pytest.fixture
def BV_0() -> BitVector:
    return BitVector(0)


@pytest.fixture
def BV_1() -> BitVector:
    return BitVector(1)


@pytest.fixture
def BV_HI() -> BitVector:
    return BitVector(0x8000_0000_0000_0000_0000_0000_0000_0000)


@pytest.fixture
def BV_SET() -> BitVector:
    return BitVector(0xFFFF_FFFF_FFFF_FFFF_FFFF_FFFF_FFFF_FFFF)


@pytest.fixture
def SixteenBitClass() -> object:
    """Returns an instance of a BitVector subclass with properties
    declared using bitvector.BitField instances.
    """

    class TestClass(BitVector):
        def __init__(self, value: int = 0):
            super().__init__(value, size=16)

        byte0 = BitField(0, 8)
        byte1 = BitField(8, 16)
        bit0 = BitField(0)
        bit1 = BitField(1)
        bit2 = BitField(2)
        bit3 = BitField(3)
        bit4 = BitField(4)
        bit5 = BitField(5)
        bit6 = BitField(6)
        bit7 = BitField(7)
        bit8 = BitField(8)
        bit9 = BitField(9)
        bitA = BitField(10)
        bitB = BitField(11)
        bitC = BitField(12)
        bitD = BitField(13)
        bitE = BitField(14)
        bitF = BitField(15)

    return TestClass
