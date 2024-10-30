import functools
import time

from loguru import logger


def timeit(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = await func(*args, **kwargs)
        end_time = time.perf_counter()
        elapsed_time = end_time - start_time
        logger.info(f"Function {func.__name__} took {elapsed_time:.8f} seconds")
        return result
    return wrapper

def log_request(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        logger.info(f"Request: {func.__name__}")
        logger.info(f"Args: {args}")
        logger.info(f"Kwargs: {kwargs}")
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