"""Credential leak scanner plugin."""

import re
from typing import List

PASSWORD_REGEX = re.compile(r"password\s*[:=]\s*(\S+)", re.IGNORECASE)


def scan(text: str) -> List[str]:
    """Search for password-like patterns in the given text.

    Parameters
    ----------
    text: str
        The text to scan.

    Returns
    -------
    List[str]
        List of found password values.
    """
    matches = PASSWORD_REGEX.findall(text)
    return matches