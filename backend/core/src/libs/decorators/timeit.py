import time
import functools

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
