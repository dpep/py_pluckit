"""
Makes the list, dict, and set built-in types into Pluckables.
Warning, this depends on the forbiddenfruit library, which
is self proclaimed to be super hacky and not production ready.
Use at your own discretion.

usage:  just import this package and you're good to go,
eg. `import pluckit.native`
"""

from .pluck import pluck

try:
    import forbiddenfruit
except ImportError:
    raise ImportError(
      'manual install needed: `pip install forbiddenfruit`'
    )

__all__ = [ 'install', 'uninstall' ]


types = [ dict, list, set ]

def install():
    for _type in types:
      forbiddenfruit.curse(_type, 'pluck', pluck)


def uninstall():
    for _type in types:
      forbiddenfruit.reverse(_type, 'pluck')


# wire it up
install()
