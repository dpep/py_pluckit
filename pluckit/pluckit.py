import re
from types import *


__all__ = [ 'pluckit' ]


split_path = re.compile(r'\.|\[|\]').split


def pluckit(obj, handle):
    if obj is None or handle is None:
        # nothing to pluck
        return None

    # function pointer
    if callable(handle):
        return handle(obj)

    # index for list-like object
    if isinstance(handle, int):
        return obj[handle]

    # strange...just, pass it through
    if not isinstance(handle, str):
        return obj[handle]

    res = obj
    for next in split_path(handle):
        if not next:
            continue

        if str.isdigit(next):
            # cast to int
            res = pluckPathItem(res, int(next))
        elif next[0] == next[-1] and (next[0] in ['"', "'"]):
            # strip quotes
            res = pluckPathItem(res, next[1:-1])
        else:
            # use as is
            res = pluckPathItem(res, next)

    return res



def pluckPathItem(obj, handle):
    # index for list-like object
    if isinstance(handle, int):
        return obj[handle]

    # dict-like object
    if hasattr(obj, 'keys'):
        return obj[handle]

    # object attribute or method
    if hasattr(obj, handle):
        attr = getattr(obj, handle)

        # if it's a method, call it
        if isinstance(attr, (
            BuiltinFunctionType, BuiltinMethodType,
            FunctionType, MethodType,
        )):
            # use return value
            return attr()

        # class attribute
        return attr

    # last chance
    if hasattr(obj, '__getitem__'):
        return obj[handle]

    raise KeyError(handle)
