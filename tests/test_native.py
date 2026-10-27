"""
Make native list / dict / set / tuple pluckable
"""

import importlib
import unittest
from collections import namedtuple

# Patching builtins leaks into every other test, so scope it to this module.
# Importing installs, and pytest imports all test modules before running any.


def setUpModule():
    importlib.import_module("pluckit.native")


def tearDownModule():
    importlib.import_module("pluckit.native").uninstall()


class NativeTest(unittest.TestCase):
    def test_list(self):
        data = [
            {"x": 1, "y": 2},
            {"x": 2, "y": 4},
            {"x": 3, "y": 6},
        ]

        self.assertEqual([1, 2, 3], data.pluck("x"))

    def test_dict(self):
        data = {
            "a": {"k": 1, "v": 2},
            "b": {"k": 3, "v": 4},
            "c": {"k": 5, "v": 6},
        }

        self.assertEqual(
            {
                "a": 2,
                "b": 4,
                "c": 6,
            },
            data.pluck("v"),
        )

    def test_set(self):
        Coordinate = namedtuple("Coordinate", ["x", "y"])  # hashable

        data = {
            Coordinate(x=1, y=2),
            Coordinate(x=2, y=4),
            Coordinate(x=3, y=6),
        }

        self.assertEqual({1, 2, 3}, data.pluck("x"))

    def test_tuple(self):
        data = (
            (1, 2),
            (3, 4),
        )

        self.assertEqual((3, 7), data.pluck(sum))

    def test_uninstall(self):
        native = importlib.import_module("pluckit.native")

        native.uninstall([frozenset])  # never installed
        native.uninstall([list, list])
        self.assertFalse(hasattr([], "pluck"))

        native.install([list])
        self.assertEqual([1], [[1]].pluck(0))


if __name__ == "__main__":
    unittest.main()
