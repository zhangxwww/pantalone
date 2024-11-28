def nop(it, *_, **__):
    return it

def patch_module(module, func_name, new_func):
    setattr(module, func_name, new_func)
