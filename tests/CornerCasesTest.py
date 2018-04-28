#!/usr/bin/python

import os
import sys
import unittest

from collections import namedtuple

sys.path = [ os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')) ] + sys.path
from pluckit import pluck


class CornerCasesTest(unittest.TestCase):
    def test_null_handle(self):
        data = {
            'a' : [1, 2],
            'b' : [3, 4],
        }

        with self.assertRaises(TypeError):
            self.assertEquals(data, pluck(data, None))


    def test_empty(self):
        self.assertEquals([], pluck([], 'k'))
        self.assertEquals([], pluck([], 'k', 'v'))

        self.assertEquals({}, pluck({}, 'k'))
        self.assertEquals({}, pluck({}, 'k', 'v'))



    def test_noop(self):
        data = [1, 2, 3]
        self.assertEquals(data, pluck(data))

        data = {'a' : 1, 'b' : 2}
        self.assertEquals(data, pluck(data))


    def test_none(self):
        self.assertEquals(None, pluck(None))
        self.assertEquals(None, pluck(None, 123))
        self.assertEquals(None, pluck(None, None))

        data = {
            None : [1, 2],
            'b' : [3, 4],
            'c' : [None, 5]
        }
        self.assertEquals(
            {
                None : 1,
                'b' : 3,
                'c' : None,
            },
            pluck(data, 0)
        )



if __name__ == '__main__':
    unittest.main()
