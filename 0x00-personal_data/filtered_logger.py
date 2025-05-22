#!/usr/bin/env python3
"""filtered_logger module"""

import os
import logging
import mysql.connector
from mysql.connector.connection import MySQLConnection
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


def get_db() -> MySQLConnection:
    """Returns a connector to the database"""
    return mysql.connector.connect(
            host=os.getenv("PERSONAL_DATA_DB_HOST", "localhost"),
            user=os.getenv("PERSONAL_DATA_DB_USERNAME", "root"),
            password=os.getenv("PERSONAL_DATA_DB_PASSWORD", ""),
            database=os.getenv("PERSONAL_DATA_DB_NAME")
            )


def main() -> None:
    """
    Obtain database connection and retrieve all rows in `users` table
    in a filtered format
    """
    connection = get_db()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()

    logger = get_logger()
    fields = (
            "name",
            "email",
            "phone",
            "ssn",
            "password",
            "ip",
            "last_login",
            "user_agent"
            )

    for row in rows:
        message = ("; ".join(f"{field}={str(value)}" for field, value in
                             zip(fields, row)) + ";")
        logger.info(message)

    cursor.close()
    connection.close()


if __name__ == "__main__":
    main()
