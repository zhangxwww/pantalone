import functools

from pydantic import BaseModel
from loguru import logger


def log_request(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        logger.info(f"Request: {func.__name__}")
        logger.info(f"Args: {[arg for arg in args if isinstance(arg, BaseModel)]}")
        logger.info(f"Kwargs: {[v for v in kwargs.values() if isinstance(v, BaseModel)]}")
        return await func(*args, **kwargs)
    return wrapper

def log_response(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        result = await func(*args, **kwargs)
        logger.info(f"Response: {func.__name__}")
        logger.info(f"Result: {result}")
        return result
    return wrapper
