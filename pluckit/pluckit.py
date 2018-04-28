from types import *


__all__ = [ 'pluckit' ]


def pluckit(obj, *handles):
    if obj == None:
        # None has nothing to pluck...
        return None

    if len(handles) == 0:
        # they don't want to pluck anything?
        return obj

    if len(handles) == 1:
        return __pluck_single(obj, handles[0])

    return [ __pluck_single(obj, handle) for handle in handles ]


def __pluck_single(obj, handle):
    # function pointer
    if callable(handle):
        return handle(obj)

    # dict-like key
    if hasattr(obj, 'has_key'):
        return obj[handle]

    # object attribute or class method
    if type(handle) == str and hasattr(obj, handle):
        attr = getattr(obj, handle)

        # make sure it's a class method, not a legit returned callable
        if isinstance(attr, (
            BuiltinFunctionType, BuiltinMethodType,
            FunctionType, MethodType,
        )):
            # use method's return value
            return attr()

        # class attribute
        return attr

    # list-like index
    if hasattr(obj, '__getitem__') and isinstance(handle, int):
        return obj[handle]

    raise TypeError('invalid handle: %s' % handle)
