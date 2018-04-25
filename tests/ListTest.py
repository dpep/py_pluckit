#!/usr/bin/python

import os
import sys
import unittest

sys.path = [ os.path.abspath(os.path.join(os.path.dirname(__file__), '..')) ] + sys.path
from pluckit import pluck


class ArrayTest(unittest.TestCase):
    def test_basic(self):
        data = [
            {'x': 1, 'y': 2},
            {'x': 2, 'y': 4},
            {'x': 3, 'y': 6},
        ]

        self.assertEquals(
            [1, 2, 3],
            pluck(data, 'x')
        )


    def test_indicies(self):
        data = [
            [0, 1, 2],
            [5, 6, 7],
        ]
        self.assertEquals(
            [0, 5],
            pluck(data, 0)
        )

        self.assertEquals(
            [ [ 0, 1 ], [ 5, 6 ] ],
            pluck(data, 0, 1)
        )


    def test_fn(self):
        # build-in
        data = [
            [1],
            [1, 2],
            [1, 2, 3],
        ]
        self.assertEquals(
            [1, 2, 3],
            pluck(data, max)
        )

        # user function
        def double(val): return val * 2
        self.assertEquals(
            [2, 4, 6],
            pluck([1, 2, 3], double),
        )

        # lambda
        self.assertEquals(
            [2, 4, 6],
            pluck([1, 2, 3], lambda x: x * 2)
        )



if __name__ == '__main__':
    unittest.main()
