from collections.abc import Iterable, Mapping
from collections.abc import Set as AbstractSet

from .pluckit import pluckit

__all__ = ["pluck"]


def pluck(collection, handle):
    if collection is None:
        # nothing to pluck
        return None

    if isinstance(collection, Mapping):
        return {k: pluckit(v, handle) for k, v in collection.items()}

    if isinstance(collection, AbstractSet):
        return {pluckit(x, handle) for x in collection}

    if isinstance(collection, tuple):
        return tuple(pluckit(x, handle) for x in collection)

    if isinstance(collection, Iterable):
        # list or list like
        return [pluckit(x, handle) for x in collection]

    raise TypeError(f"unpluckable type: {type(collection)}")
