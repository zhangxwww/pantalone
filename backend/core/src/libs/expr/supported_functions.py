import inspect

import libs.expr._supported_functions as _supported_functions

_functions = inspect.getmembers(_supported_functions, inspect.isfunction)

SUPPORTED_FUNCTIONS = {name: func for name, func in _functions}
