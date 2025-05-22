#!/usr/bin/env python3
"""filtered_logger module"""

import logging
import re
from typing import List


PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_datum(
        fields: List[str],
        redaction: str,
        message: str,
        separator: str
        ) -> str:
    """Returns obfuscated log message"""
    pattern = r"(" + "|".join(fields) + r")=.*?" + re.escape(separator)
    return re.sub(pattern, r"\1=" + redaction + separator, message)


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """ Filter values in incoming log records using `filter_datum`
        """
        log_message = super().format(record)
        return filter_datum(
                self.fields,
                self.REDACTION,
                log_message,
                self.SEPARATOR
                )


def get_logger() -> logging.Logger:
    """Returns a `logging.Logger` object"""
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    formatter = RedactingFormatter(fields=PII_FIELDS)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    logger.addHandler(stream_handler)

    return logger
