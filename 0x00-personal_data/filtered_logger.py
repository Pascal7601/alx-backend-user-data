#!/usr/bin/env python3
"""
work on logging module
"""

from typing import List, Tuple
import re
import logging
import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

load_dotenv()



PII_FIELDS: Tuple[str] = ("ssn", "password", "email", "ip", "phone")


def filter_datum(
        fields: List[str],
        redaction: str,
        message: str,
        separator: str
        ):
    """
    returns the log message obfuscated:
    """
    for field in fields:
        message = re.sub(f'{field}=.*?{separator}',
                         f'{field}={redaction}{separator}', message)
    return message


class RedactingFormatter(logging.Formatter):
    """
    Redacting Formatter class
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        record.msg = filter_datum(self.fields, self.REDACTION, record.msg, self.SEPARATOR)
        return super(RedactingFormatter, self).format(record)


def get_logger() -> logging.Logger:
    """
    create a logger object
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.addHandler(stream_handler)
    return logger


def get_db():
    """
    connect to the database
    """
    connection = {
        'user': os.getenv('PERSONAL_DATA_DB_USERNAME'),
        'password': os.getenv('PERSONAL_DATA_DB_PASSWORD'),
        'host': os.getenv('PERSONAL_DATA_DB_HOST'),
        'port': 3308,
        'use_pure': True,
        'ssl_disabled': True
    }

    try:
        db = mysql.connector.connect(**connection)
        print("Connection successful:", db)
        return db
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None


def main():
    STATEMENT = """
    SELECT * FROM users;
"""
    conn = get_db()

    cursor = conn.cursor()
    cursor.execute("USE my_db")
    cursor.execute(STATEMENT)
    users = cursor.fetchall()
    for user in users:
        get_logger().info(user)
        print(user)

    cursor.close()
    conn.close()

main()



