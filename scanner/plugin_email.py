"""Email leak scanner plugin."""

import re
from typing import List

EMAIL_REGEX = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")


def scan(text: str) -> List[str]:
    """Search for email addresses in the given text.

    Parameters
    ----------
    text: str
        The text to scan.

    Returns
    -------
    List[str]
        List of found email addresses.
    """
    return EMAIL_REGEX.findall(text)