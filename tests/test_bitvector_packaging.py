"""
"""

import pytest


@pytest.mark.fast
def test_bitvector_import_version():

    from bitvector.__version__ import __version__
