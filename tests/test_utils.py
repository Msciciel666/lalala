from utils.helpers import normalize_url


def test_normalize_url_adds_scheme():
    """normalize_url should prefix http if missing."""
    assert normalize_url("example.com") == "http://example.com"


def test_normalize_url_keeps_scheme():
    """normalize_url should return URL unchanged if scheme exists."""
    assert normalize_url("https://example.com") == "https://example.com"
