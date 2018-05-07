#!/usr/bin/python

import os
import sys
import unittest

from collections import namedtuple

sys.path = [ os.path.abspath(os.path.join(os.path.dirname(__file__), '..')) ] + sys.path
from pluckit import pluck



class TupleTest(unittest.TestCase):
    def test_basic(self):
        data = (
            [ 1, 2 ],
            [ 3, 4 ],
        )

        self.assertEquals(
            (1, 3),
            pluck(data, 0)
        )

        self.assertEquals(
            (2, 4),
            pluck(data, max)
        )



if __name__ == '__main__':
    unittest.main()
