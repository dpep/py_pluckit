#!/usr/bin/python

import os
import sys
import unittest

sys.path = [ os.path.abspath(os.path.join(os.path.dirname(__file__), '..')) ] + sys.path
from pluckit import Pluckable


class PList(list, Pluckable): pass

class ArrayTest(unittest.TestCase):
    def test_basic(self):
        data = PList([
            {'k': 1},
            {'k': 2},
            {'k': 3},
        ])

        self.assertEquals(
            [1, 2, 3],
            data.pluck('k')
        )


    def test_indicies(self):
        data = PList([
            [0, 1, 2],
            [5, 6, 7],
        ])
        self.assertEquals(
            [0, 5],
            data.pluck(0)
        )

        self.assertEquals(
            [ [ 0, 1 ], [ 5, 6 ] ],
            data.pluck(0, 1)
        )


    def test_fn(self):
        # build-in
        data = PList([
            [1],
            [1, 2],
            [1, 2, 3],
        ])
        self.assertEquals(
            [1, 2, 3],
            data.pluck(max)
        )

        # user function
        def double(val): return val * 2
        self.assertEquals(
            [2, 4, 6],
            PList([1, 2, 3]).pluck(double),
        )

        # lambda
        self.assertEquals(
            [2, 4, 6],
            PList([1, 2, 3]).pluck(lambda x: x * 2)
        )


if __name__ == '__main__':
    unittest.main()
