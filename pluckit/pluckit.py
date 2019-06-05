from types import *


__all__ = [ 'pluckit' ]


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

    # dict-like object
    if hasattr(obj, 'keys'):
        return obj[handle]

    if not isinstance(handle, str):
        raise TypeError('invalid handle type: %s: %s' % (type(handle), handle))

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

    raise KeyError(handle)
