#!/usr/bin/python

import os
import sys
import unittest

from collections import namedtuple

sys.path = [ os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')) ] + sys.path
from pluckit import pluck


class CornerCasesTest(unittest.TestCase):
    def test_null_handle(self):
        data = [1, 2, 3]
        self.assertEqual(data, pluck(data, None))


    def test_empty(self):
        self.assertEqual([], pluck([], 'k'))
        self.assertEqual({}, pluck({}, 'k'))
        self.assertEqual(set(), pluck(set(), 'k'))


    def test_null(self):
        self.assertEqual(None, pluck(None, None))
        self.assertEqual(None, pluck(None, 123))


    def test_null_values(self):
        data = {
            None : [1, 2],
            'b' : [3, 4],
            'c' : [None, 5]
        }
        self.assertEqual(
            {
                None : 1,
                'b' : 3,
                'c' : None,
            },
            pluck(data, 0)
        )



if __name__ == '__main__':
    unittest.main()
