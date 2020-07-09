"""
"""

import pytest

from bitvector import BitVector


@pytest.fixture
def BV_0() -> BitVector:
    return BitVector(0)


@pytest.fixture
def BV_1() -> BitVector:
    return BitVector(1)


@pytest.fixture
def BV_HI() -> BitVector:
    return BitVector(0x8000_0000_0000_0000_0000_0000_0000_0000)
