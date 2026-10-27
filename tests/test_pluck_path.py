import math
import unittest
from types import MappingProxyType, SimpleNamespace

from pluckit import pluck
from pluckit.pluckit import ATTR, BARE, ITEM, STAR, parse_path, pluckit


class PluckPathTest(unittest.TestCase):
    def test_parse_path(self):
        self.assertEqual(((BARE, "a"),), parse_path("a"))
        self.assertEqual(((ITEM, "a"),), parse_path("[a]"))
        self.assertEqual(((ITEM, "a"),), parse_path('["a"]'))
        self.assertEqual(((ITEM, "a"),), parse_path("['a']"))
        self.assertEqual(((ITEM, "a"),), parse_path("[ a ]"))
        self.assertEqual(((ITEM, "a"),), parse_path('[ "a" ]'))
        self.assertEqual(((BARE, "0"),), parse_path("0"))
        self.assertEqual(((ITEM, 0),), parse_path("[0]"))
        self.assertEqual(((ITEM, "0"),), parse_path('["0"]'))
        self.assertEqual(((ITEM, slice(1, None)),), parse_path("[1:]"))

        self.assertEqual(((BARE, "a"), (ATTR, "b")), parse_path("a.b"))
        self.assertEqual(((BARE, "a"), (ATTR, "0")), parse_path("a.0"))
        self.assertEqual(((ITEM, 0), (ITEM, 1)), parse_path("[0][1]"))

        self.assertEqual(((STAR, None),), parse_path("*"))
        self.assertEqual(((STAR, None),), parse_path("[*]"))
        self.assertEqual(((ITEM, "*"),), parse_path('["*"]'))
        self.assertEqual(((BARE, "a"), (STAR, None)), parse_path("a.*"))
        self.assertEqual(((BARE, "a"), (STAR, None)), parse_path("a[*]"))
        self.assertEqual(((STAR, None), (ATTR, "a")), parse_path("*.a"))

        # quoted keys may contain anything but their own quote
        self.assertEqual(((ITEM, "a].b"), (ATTR, "c")), parse_path('["a].b"].c'))
        self.assertEqual(((ITEM, '"'),), parse_path("['\"']"))
        self.assertEqual(((ITEM, '"'),), parse_path('["]'))

    def test_path_errors(self):
        bad_paths = [
            "",
            ".",
            "[]",
            "[ ]",
            "[",
            "]",
            ".[",
            ".]",
            "..",
            ".[]",
            ".[a]",
            ".[0]",
            "0.",
            "*.",
            "*[",
            "a b",
        ]
        for path in bad_paths:
            with self.subTest(path=path), self.assertRaises(ValueError):
                parse_path(path)

        # validated up front, regardless of the data
        with self.assertRaises(ValueError):
            pluckit([], "*.a.")
        with self.assertRaises(ValueError):
            pluck([], "!!bad")

    def test_basic(self):
        data = [[1, 2], [3], 4]

        self.assertEqual(1, pluckit(data, "0[0]"))
        self.assertEqual(2, pluckit(data, "0[1]"))
        self.assertEqual(3, pluckit(data, "1[0]"))

        self.assertEqual(4, pluckit(data, "-1"))
        self.assertEqual(2, pluckit(data, "0[-1]"))

        data = {"a": {"b": 1}, "c": {"d": 1}}
        self.assertEqual(1, pluckit(data, 'a["b"]'))
        self.assertEqual(1, pluckit(data, "a['b']"))

    def test_fns(self):
        class Foo:
            def foo(self):
                return "foo"

        data = {"a": {"b": 1}, "c": {"d": Foo()}}

        self.assertEqual(["a", "c"], list(pluckit(data, ".keys")))

        self.assertEqual(["b"], list(pluckit(data, "a.keys")))

        self.assertEqual([1], list(pluckit(data, "a.values")))

        self.assertEqual("foo", pluckit(data, "c[d].foo"))

        self.assertEqual("Foo", pluckit(data, "c[d].__class__.__name__"))

        # method-wrappers are methods too
        self.assertEqual(3, pluckit("abc", ".__len__"))
        self.assertEqual(3, pluckit("abc", "__len__"))

        # classes are callable, but not methods
        self.assertIs(int, pluckit(SimpleNamespace(kind=int), "kind"))

    def test_errors(self):
        data = {"a": []}

        with self.assertRaises(IndexError):
            pluckit(data, "a[0]")

        with self.assertRaises(AttributeError):
            pluckit(data, "a.0")

        with self.assertRaises(AttributeError):
            pluckit(data, "a.z")

        with self.assertRaises(KeyError):
            pluckit(data, "z")

        with self.assertRaises(AttributeError):
            pluckit(data, ".z")

    def test_empty_list(self):
        with self.assertRaises(IndexError):
            pluckit([], "0")
        with self.assertRaises(IndexError):
            pluckit([], "-1")
        with self.assertRaises(AttributeError):
            pluckit([], ".0")

    def test_empty_dict(self):
        with self.assertRaises(KeyError):
            pluckit({}, "a")

        with self.assertRaises(KeyError):
            pluckit({}, "0")

    def test_wildcard(self):
        data = [[1], [2]]
        self.assertEqual(data, pluckit(data, "*"))
        self.assertEqual(data, pluckit(data, ".*"))

        self.assertEqual(data, pluckit(data, "*.*"))
        self.assertEqual(data, pluckit(data, "*[*]"))
        self.assertEqual(data, pluckit(data, ".*.*"))

        self.assertEqual([1, 2], pluckit(data, "*[0]"))

        data = {"a": {"b": 1}}
        self.assertEqual([{"b": 1}], pluckit(data, "*"))
        self.assertEqual([{"b": 1}], pluckit(data, ".*"))

        self.assertEqual([1], pluckit(data, "*[b]"))
        self.assertEqual([1], pluckit(data, "a[*]"))

        self.assertEqual([[1]], pluckit(data, "*[*]"))
        self.assertEqual([[1]], pluckit(data, "*.*"))

    def test_wildcard_advanced(self):
        data = {
            "a": {"k": 1, "v": [1, 2]},
            "b": {"k": 2, "v": [3, 4]},
        }

        self.assertEqual([1, 2], pluckit(data, "*[k]"))

        self.assertEqual([[1, 2], [3, 4]], pluckit(data, "*[v]"))

        self.assertEqual([[1, 2], [3, 4]], pluckit(data, "*[v]*"))

        self.assertEqual([1, 3], pluckit(data, "*[v][0]"))

    def test_wildcard_empty(self):
        self.assertEqual([], pluckit([], "*"))
        self.assertEqual([], pluckit({}, "*"))

        self.assertEqual([], pluckit([], "*.*"))
        self.assertEqual([], pluckit({}, "*.*"))

        self.assertEqual([], pluckit([], "*.a"))

    def test_wildcard_errors(self):
        data = {"a": [], "b": 2}

        with self.assertRaises(KeyError):
            pluckit(data, '["*"]')

        with self.assertRaises(TypeError):
            pluckit(data, 'a["*"]')

        with self.assertRaises(TypeError):
            pluckit(data, "b.*")

        with self.assertRaises(ValueError):
            pluckit(data, "*.")

    def test_wildcard_mappings(self):
        data = MappingProxyType({"a": 1, "b": 2})
        self.assertEqual([1, 2], pluckit(data, "*"))

        # only Mappings have their values() iterated
        class Row(list):
            values = "not a method"

        self.assertEqual([1, 2], pluckit(Row([1, 2]), "*"))

    def test_quoted_keys(self):
        self.assertEqual(1, pluckit({"a].b": {"c": 1}}, '["a].b"][c]'))
        self.assertEqual(1, pluckit({'"': 1}, "['\"']"))

    def test_whitespace(self):
        self.assertEqual(1, pluckit([0, 1], "[ 1 ]"))
        self.assertEqual([1, 2], pluckit([0, 1, 2], "[ 1:3 ]"))
        self.assertEqual(1, pluckit({" a ": 1}, '[" a "]'))

    def test_odd_equality(self):
        # bare names must not depend on the object's __eq__
        self.assertTrue(math.isnan(pluckit(float("nan"), "real")))

        class Never:
            x = 1

            def __eq__(self, other):
                return False

        self.assertEqual(1, pluckit(Never(), "x"))

    def test_wildcard_none(self):
        self.assertEqual([None, 1], pluckit([None, [1]], "*[0]"))

    def test_slice(self):
        data = [0, 1, 2, 3]

        self.assertEqual(
            data[1:3],  # [ 1, 2 ]
            pluckit(data, "[1:3]"),
        )

        self.assertEqual(data[2:], pluckit(data, "[2:]"))

        self.assertEqual(data[:2], pluckit(data, "[:2]"))

        self.assertEqual(data[::2], pluckit(data, "[::2]"))

        self.assertEqual(data[:], pluckit(data, "[:]"))

        self.assertEqual(data[::], pluckit(data, "[::]"))


if __name__ == "__main__":
    unittest.main()
