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
            {'x': 1, 'y': 2},
            {'x': 2, 'y': 4},
            {'x': 3, 'y': 6},
        ])

        self.assertEquals(
            [1, 2, 3],
            data.pluck('x')
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


    def test_clone(self):
        class MyList(PList, object):
            def __init__(self, val): self.val = val

        data = MyList(123)
        data += [1, 2, 3]

        self.assertEquals(
            MyList,
            type(data)
        )
        self.assertEquals(123, data.val)

        self.assertEquals(
            MyList,
            type(data.pluck(str))
        )
        self.assertEquals(123, data.pluck(str).val)


if __name__ == '__main__':
    unittest.main()
