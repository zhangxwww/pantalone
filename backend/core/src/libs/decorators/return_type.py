from copy import deepcopy
from functools import wraps

import numpy as np


def return_numpy_array(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return np.array(func(*args, **kwargs))
    return wrapper

def yield_numpy_array(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        yield from (np.array(x) for x in func(*args, **kwargs))
    return wrapper

def return_copy_async(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        res = await func(*args, **kwargs)
        return deepcopy(res)
    return wrapper
