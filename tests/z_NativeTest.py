#!/usr/bin/env python

"""
Make native list / dict / set pluckable

Warning: This test must run last because it's modification
of builtin types will effect other tests, hence the z_ prefix
in it's file name.
"""

import os
import sys
import unittest

from collections import namedtuple

sys.path = [ os.path.abspath(os.path.join(os.path.dirname(__file__), '..')) ] + sys.path
import pluckit.native


class NativeTest(unittest.TestCase):
    def test_list(self):
        data = [
            {'x': 1, 'y': 2},
            {'x': 2, 'y': 4},
            {'x': 3, 'y': 6},
        ]

        self.assertEqual(
            [1, 2, 3],
            data.pluck('x')
        )


    def test_dict(self):
        data = {
            'a': { 'k': 1, 'v': 2 },
            'b': { 'k': 3, 'v': 4 },
            'c': { 'k': 5, 'v': 6 },
        }

        self.assertEqual(
            {
                'a': 2,
                'b': 4,
                'c': 6,
            },
            data.pluck('v')
        )


    def test_set(self):
        Coordinate = namedtuple('Coordinate', ['x', 'y'])  # hashable

        data = {
            Coordinate(x=1, y=2),
            Coordinate(x=2, y=4),
            Coordinate(x=3, y=6),
        }

        self.assertEqual(
            {1, 2, 3},
            data.pluck('x')
        )


    def test_tuple(self):
        data = (
            (1, 2),
            (3, 4),
        )

        self.assertEqual(
            (3, 7),
            data.pluck(sum)
        )




if __name__ == '__main__':
    unittest.main()
