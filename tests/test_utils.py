import pytest

from aag import utils


def test_get_rate():
    assert isinstance(utils.get_rate("twd", "jpy"), float)


def test_get_rate_failed():
    with pytest.raises(RuntimeError):
        utils.get_rate("ntd", "jpy")
