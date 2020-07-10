"""
"""

import pytest

from bitvector import BitVector


@pytest.mark.fast
def test_bitvector_method_set(BV_0: BitVector):

    assert BV_0 == 0
    BV_0.set()
    assert all(BV_0)


@pytest.mark.fast
def test_bitvector_method_clear(BV_SET: BitVector):

    assert all(BV_SET)
    BV_SET.clear()
    assert not any(BV_SET)


@pytest.mark.fast
@pytest.mark.parametrize("offset", list(range(0, 128)))
def test_bitvector_method_toggle(offset: int, BV_0: BitVector):

    assert BV_0[offset] == 0

    BV_0.toggle(offset)
    assert BV_0[offset] == 1

    BV_0.toggle(offset)
    assert BV_0[offset] == 0
