import functools
import inspect
import re
from collections.abc import Mapping

__all__ = ["pluckit"]


def pluckit(obj, handle):
    if obj is None or handle is None:
        # nothing to pluck
        return None

    # function pointer, behave like map()
    if callable(handle):
        return handle(obj)

    # index, key, or slice: just pass it through
    if not isinstance(handle, str):
        return obj[handle]

    return _walk(obj, parse_path(handle))


# step kinds
BARE = "bare"  # unadorned name, resolved by heuristics.  only ever the first step
ATTR = "attr"
ITEM = "item"
STAR = "star"

step_regex = re.compile(
    r"""(
        (?P<dot>\.)?(?P<handle>\*|-?\d+|[a-z_][a-z0-9_]*)
        | \[(?: "(?P<dq>[^"]*)" | '(?P<sq>[^']*)' | (?P<subscript>.+?) )\]
    )(?=[\*\.\[]|\Z)""",
    flags=re.IGNORECASE | re.VERBOSE,
)
is_numeric = re.compile(r"^-?\d+$").match
is_slice = re.compile(r"^(-?\d+)?:(-?\d+)?:?(-?\d+)?$").match


@functools.lru_cache(maxsize=256)
def parse_path(path):
    """Parse a path like `a[0].b` into a tuple of (kind, key) steps."""
    if not path:
        raise ValueError("invalid path syntax: empty path")

    steps = []
    pos = 0
    while pos < len(path):
        match = step_regex.match(path, pos)
        if not match:
            raise ValueError("invalid path syntax: " + path[pos:])
        pos = match.end()

        handle, subscript = match.group("handle"), match.group("subscript")
        quoted = match.group("dq")
        if quoted is None:
            quoted = match.group("sq")

        if "*" in (handle, subscript):
            steps.append((STAR, None))
        elif handle is not None:
            steps.append((ATTR if match.group("dot") else BARE, handle))
        elif quoted is not None:
            steps.append((ITEM, quoted))
        elif is_numeric(subscript):
            steps.append((ITEM, int(subscript)))
        elif is_slice(subscript):
            parts = (int(x) if x else None for x in subscript.split(":"))
            steps.append((ITEM, slice(*parts)))
        else:
            steps.append((ITEM, subscript))

    return tuple(steps)


def _walk(obj, steps):
    for i, (kind, key) in enumerate(steps):
        if kind is STAR:
            values = obj.values() if isinstance(obj, Mapping) else obj
            rest = steps[i + 1 :]
            # None values short-circuit, same as pluckit()
            return [None if x is None else _walk(x, rest) for x in values]

        if kind is ATTR:
            obj = _pluck_attr(obj, key)
        elif kind is ITEM:
            obj = obj[key]
        else:
            obj = _pluck_bare(obj, key)

    return obj


def _pluck_bare(obj, name):
    # unspecified type, use heuristics
    if hasattr(obj, "keys"):
        return obj[name]

    if hasattr(obj, name):
        # seems legit since attr exists, so go with it
        return _pluck_attr(obj, name)

    if hasattr(obj, "__getitem__"):
        # assume name is a subscript: list-like index or dict-like key
        return obj[int(name)] if is_numeric(name) else obj[name]

    raise ValueError("invalid handle: " + name)


def _pluck_attr(obj, handle):
    attr = getattr(obj, handle)

    if inspect.isroutine(attr):
        # call it and use return value
        return attr()

    # otherwise, it's a class attribute
    return attr
