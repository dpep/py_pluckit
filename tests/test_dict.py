import unittest
from collections import ChainMap
from types import MappingProxyType

from pluckit import pluck


class DictTest(unittest.TestCase):
    def test_basic(self):
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
            pluck(data, "v"),
        )

    def test_indicies(self):
        data = {
            "a": [0, 1],
            "b": [5, 6],
        }

        self.assertEqual(
            {
                "a": 1,
                "b": 6,
            },
            pluck(data, 1),
        )

    def test_mappings(self):
        data = {"a": [0, 1], "b": [5, 6]}

        self.assertEqual({"a": 1, "b": 6}, pluck(MappingProxyType(data), 1))
        self.assertEqual({"a": 1, "b": 6}, pluck(ChainMap(data), 1))


if __name__ == "__main__":
    unittest.main()
