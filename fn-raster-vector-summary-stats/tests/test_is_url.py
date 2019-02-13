from preprocess_helpers import is_url


def test_is_url():
    url = 'http://example.com'
    actual = is_url(url)
    expected = True
    assert actual == expected


def test_is_not_url():
    url = 'something_broken'
    actual = is_url(url)
    expected = False
    assert actual == expected


def test_is_empty():
    url = None
    actual = is_url(url)
    expected = False
    assert actual == expected
