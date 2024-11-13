import asyncio
import random
from functools import wraps

from sqlalchemy.exc import OperationalError
from loguru import logger


def _retry_when_db_locked(retry_times: int = 3):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            for i in range(retry_times):
                try:
                    return await func(*args, **kwargs)
                except OperationalError as e:
                    if 'database is locked' in str(e):
                        logger.warning(f'Error: {e}')
                        logger.warning(f'Retry {i + 1}/{retry_times}')
                        db = args[0]
                        await db.rollback()
                        await asyncio.sleep(random.uniform(1, 3))
                    else:
                        raise e
        return wrapper
    return decorator
