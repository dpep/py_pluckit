#!/usr/bin/python

import os
import sys
import unittest

from collections import namedtuple

sys.path = [ os.path.abspath(os.path.join(os.path.dirname(__file__), '..')) ] + sys.path
from pluckit.pluckable import *


class PluckablesTest(unittest.TestCase):
    def test_list(self):
        data = PluckableList([
            {'x': 1, 'y': 2},
            {'x': 2, 'y': 4},
            {'x': 3, 'y': 6},
        ])

        self.assertEquals(
            [1, 2, 3],
            data.pluck('x')
        )

        # type is preserved
        self.assertIsInstance(data.pluck('x'), list)


    def test_dict(self):
        data = PluckableDict({
            'a': { 'k': 1, 'v': 2 },
            'b': { 'k': 3, 'v': 4 },
            'c': { 'k': 5, 'v': 6 },
        })

        self.assertEquals(
            {
                'a': 2,
                'b': 4,
                'c': 6,
            },
            data.pluck('v')
        )

        # type is preserved
        self.assertIsInstance(data.pluck('v'), dict)


    def test_set(self):
        Coordinate = namedtuple('Coordinate', ['x', 'y'])  # hashable

        data = PluckableSet({
            Coordinate(x=1, y=2),
            Coordinate(x=2, y=4),
            Coordinate(x=3, y=6),
        })

        self.assertEquals(
            {1, 2, 3},
            data.pluck('x')
        )

        # type is preserved
        self.assertIsInstance(data.pluck('x'), set)


    def test_tuple(self):
        data = PluckableTuple([
            (1, 2),
            (3, 4),
        ])

        self.assertEquals(
            (3, 7),
            data.pluck(sum)
        )

        # type is preserved
        self.assertIsInstance(data.pluck(sum), tuple)



if __name__ == '__main__':
    unittest.main()
