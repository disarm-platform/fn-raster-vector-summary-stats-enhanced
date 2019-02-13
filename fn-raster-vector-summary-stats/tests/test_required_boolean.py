import pytest

from preprocess_helpers import required_boolean


def test_broken():
    params = {'egg': 'false'}
    with pytest.raises(ValueError):
        required_boolean('egg', params)


def test_true():
    params = {'egg': True}
    actual = required_boolean('egg', params)
    expected = None
    assert actual == expected


def test_false():
    params = {'egg': False}
    actual = required_boolean('egg', params)
    expected = None
    assert actual == expected
