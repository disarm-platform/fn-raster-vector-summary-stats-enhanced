import pytest

from preprocess_helpers import required_exists


def test_exists():
    params = {'exists': 'irrelevant value'}
    actual = required_exists('exists', params)
    expected = None
    assert actual == expected


def test_not_exists():
    params = {'not_exists': 'irrelevant value'}
    with pytest.raises(ValueError):
        required_exists('exists', params)
