"""
"""

import pytest

from bitvector import BitVector


@pytest.fixture
def zeros() -> int:
    return 0x0000_0000_0000_0000_0000_0000_0000_0000


@pytest.fixture
def ones() -> int:
    return 0xFFFF_FFFF_FFFF_FFFF_FFFF_FFFF_FFFF_FFFF


@pytest.fixture
def alphas() -> int:
    return 0xAAAA_AAAA_AAAA_AAAA_AAAA_AAAA_AAAA_AAAA


@pytest.fixture
def fives() -> int:
    return 0x5555_5555_5555_5555_5555_5555_5555_5555
