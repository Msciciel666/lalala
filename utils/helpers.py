"""Utility helper functions."""

from urllib.parse import urlparse


def normalize_url(url: str) -> str:
    """Return a normalized URL with an HTTP scheme if missing.

    Parameters
    ----------
    url: str
        The URL to normalize.

    Returns
    -------
    str
        The normalized URL.
    """
    parsed = urlparse(url)
    if not parsed.scheme:
        return f"http://{url}"
    return url
