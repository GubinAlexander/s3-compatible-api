from functools import wraps
from src.logger import logger


def log_request(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        for header in kwargs["request"]["headers"]:
            logger.info(header)
        return func(*args, **kwargs)
    return wrapper
