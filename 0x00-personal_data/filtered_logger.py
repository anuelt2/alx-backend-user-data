#!/usr/bin/env python3
"""filtered_logger module"""

import re
from typing import List


def filter_datum(
        fields: List[str],
        redaction: str,
        message: str,
        separator: str
        ) -> str:
    """Returns obfuscated log message"""
    pattern = r"(" + "|".join(fields) + r")=.*?" + re.escape(separator)
    return re.sub(pattern, r"\1=" + redaction + separator, message)
