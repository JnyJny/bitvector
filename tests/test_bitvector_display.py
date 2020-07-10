"""
"""

import pytest

from bitvector import BitVector


@pytest.mark.fast
def test_bitvector_repr():

    bv = BitVector()
    repr_value = repr(bv)

    assert "BitVector" in repr_value
    assert "128" in repr_value


@pytest.mark.fast
@pytest.mark.parametrize("given", [0, 0xDEADBEEFBADC0FFEE, (1 << 128) - 1,])
def test_bitvector_str(given):

    bv = BitVector(given)
    str_value = str(bv)

    assert str_value.startswith("0x")
    assert int(str_value, 16) == bv.value


@pytest.mark.fast
@pytest.mark.parametrize("given", [0, 0xDEADBEEFBADC0FFEE, (1 << 128) - 1,])
def test_bitvector_bin_property(given):

    bv = BitVector()
    bin_value = bv.bin

    assert bin_value.startswith("0b")
    assert int(bin_value, 2) == bv.value


@pytest.mark.fast
@pytest.mark.parametrize("given", [0, 0xDEADBEEFBADC0FFEE, (1 << 128) - 1,])
def test_bitvector_hex_property(given):

    bv = BitVector()
    hex_value = bv.hex

    assert hex_value.startswith("0x")
    assert int(hex_value, 16) == bv.value


@pytest.mark.fast
@pytest.mark.parametrize("value", [1 << p for p in range(0, 128)])
def test_bitvector_bytes_property(value):

    bv = BitVector(value)
    bv_bytes = bv.bytes

    test = int.from_bytes(bv_bytes, "big")

    assert isinstance(bv_bytes, bytes)
    assert len(bv_bytes) == len(bv) / 8
    assert test == bv
