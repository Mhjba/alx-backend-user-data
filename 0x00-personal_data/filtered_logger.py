#!/usr/bin/env python3
""" A module for filtering logs. """

import re
import os
from typing import List
import logging
import mysql.connector
from logging import StreamHandler


PII_FIELDS = ("name", "email", "phone", "ssn", "password")


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """ Formats the log record """
        mess = super(RedactingFormatter, self).format(record)
        form = filter_datum(self.fields, self.REDACTION, mess, self.SEPARATOR)
        return form


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """ Filters a log line. """
    for field in fields:
        message = re.sub(rf"{re.escape(field)}=(.*?){re.escape(separator)}",
                         f"{field}={redaction}{separator}", message)
    return message


def get_logger() -> logging.Logger:
    """ Creates a new logger. """
    logger = logging.getLogger("user_data")
    handler = logging.StreamHandler()
    handler.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.setLevel(logging.INFO)
    logger.propagate = False
    logger.addHandler(handler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """ Returns a connector to the database """
    host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    name = os.getenv("PERSONAL_DATA_DB_NAME", "")
    user = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    password = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
    conn = mysql.connector.connect(
        host=host,
        port=3306,
        user=user,
        password=password,
        database=name,
    )
    return conn


def main() -> None:
    """
    Main function to retrieve data from database
    """
    db = get_db()
    mess = db.cursor()
    mess.execute("SELECT * FROM users;")
    for row in mess:
        message = f"name={row[0]}; email={row[1]}; phone={row[2]}; " +\
            f"ssn={row[3]}; password={row[4]};ip={row[5]}; " +\
            f"last_login={row[6]}; user_agent={row[7]};"
        print(message)
    mess.close()
    db.close()
