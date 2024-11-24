import time
import functools

from sqlalchemy.ext.asyncio import AsyncSession


class CacheWithExpiration:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(CacheWithExpiration, cls).__new__(cls)
        return cls._instance

    def __init__(self, expiration_time: int = 3600):
        if not hasattr(self, 'initialized'):
            self.expiration_time = expiration_time
            self.cache = {}
            self.initialized = True

    def __call__(self, func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            key = self._key(func, *args, **kwargs)
            if key in self.cache:
                if time.time() - self.cache[key]['time'] < self.expiration_time:
                    return self.cache[key]['value']

            result = await func(*args, **kwargs)
            self.cache[key] = {'value': result, 'time': time.time()}
            return result
        return wrapper

    @staticmethod
    def _key(func, *args, **kwargs):
        args = [str(arg) for arg in args if not isinstance(arg, AsyncSession)]
        kwargs = [f"{k}={v}" for k, v in kwargs.items() if not isinstance(v, AsyncSession)]
        return f"{func.__name__}--{'-'.join(args)}--{'-'.join(kwargs)}"
