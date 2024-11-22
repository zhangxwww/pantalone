import time
import functools

from pydantic import BaseModel
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession


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


class CacheWithExpiration:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(CacheWithExpiration, cls).__new__(cls)
        return cls._instance

    def __init__(self, expiration_time: int = 3600):
        if not hasattr(self, 'initialized'):  # 防止多次初始化
            self.expiration_time = expiration_time
            self.cache = {}
            self.initialized = True

    def __call__(self, func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            key = self._key(func, *args, **kwargs)
            if key in self.cache:
                if time.time() - self.cache[key]['time'] < self.expiration_time:
                    logger.info(f"Cache hit: {key}")
                    return self.cache[key]['value']

            logger.info(f"Cache miss: {key}")
            result = await func(*args, **kwargs)
            self.cache[key] = {'value': result, 'time': time.time()}
            return result
        return wrapper

    @staticmethod
    def _key(func, *args, **kwargs):
        args = [str(arg) for arg in args if not isinstance(arg, AsyncSession)]
        kwargs = [f"{k}={v}" for k, v in kwargs.items() if not isinstance(v, AsyncSession)]
        return f"{func.__name__}--{'-'.join(args)}--{'-'.join(kwargs)}"
