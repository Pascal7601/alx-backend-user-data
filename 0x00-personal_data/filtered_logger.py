from typing import List, Tuple
import re
import logging

PII_FIELDS: Tuple[str] = ("ssn", "password", "user_agent", "ip", "phone")

def filter_datum(
        fields: List[str],
        redaction: str,
        messages: str,
        separator: str
        ):
    """
    returns the log message obfuscated:
    """
    for field in fields:
        message = re.sub(f'{field}=.*?{separator}', f'{field}={redaction}{separator}', f'{messages}')
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
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.addHandler(stream_handler)
    return logger


