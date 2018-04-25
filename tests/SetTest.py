#!/usr/bin/python

import os
import sys
import unittest

from collections import namedtuple

sys.path = [ os.path.abspath(os.path.join(os.path.dirname(__file__), '..')) ] + sys.path
from pluckit import pluck


Coordinate = namedtuple('Coordinate', ['x', 'y'])  # hashable


class SetTest(unittest.TestCase):
    def test_basic(self):
        data = {
            Coordinate(x=1, y=2),
            Coordinate(x=2, y=4),
            Coordinate(x=3, y=6),
        }

        self.assertEquals(
            {1, 2, 3},
            pluck(data, 'x')
        )

        self.assertEquals(
            { (1, 2), (2, 4), (3, 6) },
            pluck(data, 'x', 'y')
        )



if __name__ == '__main__':
    unittest.main()
