#!/usr/bin/python

import os
import sys
import unittest

from collections import namedtuple

sys.path = [ os.path.abspath(os.path.join(os.path.dirname(__file__), '..')) ] + sys.path
from pluckit import Pluckable


class PSet(set, Pluckable): pass
Coordinate = namedtuple('Coordinate', ['x', 'y'])  # hashable


class SetTest(unittest.TestCase):
    def test_basic(self):
        data = PSet({
            Coordinate(x=1, y=2),
            Coordinate(x=2, y=4),
            Coordinate(x=3, y=6),
        })

        self.assertEquals(
            {1, 2, 3},
            data.pluck('x')
        )


    def test_type(self):
        self.assertEquals(
            PSet,
            type(PSet([1, 2, 3]).pluck(str))
        )


    def test_clone(self):
        class MySet(PSet, object):
            def __init__(self, val): self.val = val

        data = MySet(123)
        data.update({1, 2, 3})

        self.assertEquals(123, data.val)

        self.assertEquals(
            {'1', '2', '3'},
            data.pluck(str)
        )

        self.assertEquals(
            MySet,
            type(data.pluck(str))
        )

        self.assertEquals(
            123,
            data.pluck(str).val
        )


if __name__ == '__main__':
    unittest.main()
