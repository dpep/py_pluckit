#!/usr/bin/python

import os
import sys
import unittest

from collections import defaultdict

sys.path = [ os.path.abspath(os.path.join(os.path.dirname(__file__), '..')) ] + sys.path
from pluckit import Pluckable


class PDict(dict, Pluckable): pass

class DictTest(unittest.TestCase):
    def test_basic(self):
        data = PDict({
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

        self.assertEquals(
            {
                'a': [ 1, 2 ],
                'b': [ 3, 4 ],
                'c': [ 5, 6 ],
            },
            data.pluck('k', 'v')
        )


    def test_indicies(self):
        data = PDict({
            'a': [ 0, 1 ],
            'b': [ 5, 6 ],
        })

        self.assertEquals(
            {
                'a': 1,
                'b': 6,
            },
            data.pluck(1)
        )


    def test_clone(self):
        class PDDict(defaultdict, Pluckable): pass
        data = PDDict(lambda: 123)

        self.assertEquals(
            123,
            data['zzz']
        )

        data.update({
            'a': 1,
            'b': 2,
            'c': 3,
        })

        # type is preserved
        self.assertEquals(
            PDDict,
            type(data.pluck(str))
        )

        # default value is preserved
        self.assertEquals(
            123,
            data['zzz']
        )


if __name__ == '__main__':
    unittest.main()
