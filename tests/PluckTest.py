#!/usr/bin/env python

import os
import sys
import unittest

sys.path = [ os.path.abspath(os.path.join(os.path.dirname(__file__), '..')) ] + sys.path
from pluckit.pluckit import pluckit


class PluckTest(unittest.TestCase):
    def test_list(self):
        data = [ 0, 1, 2, 3 ]

        self.assertEqual(
            3,
            pluckit(data, 3),
        )

        self.assertEqual(
            list,
            pluckit(data, '__class__'),
        )

        self.assertEqual(4, len(data))
        self.assertEqual(
            3,
            pluckit(data, 'pop'),
        )
        self.assertEqual(3, len(data))

        self.assertEqual(
            3,
            pluckit(data, len),
        )

        self.assertEqual(
            3,  # 0 + 1 + 2
            pluckit(data, lambda x: sum(x))
        )


    def test_dict(self):
        abc = { 'a' : 1, 'b' : 2, 'c' : 3 }

        self.assertEqual(
            1,
            pluckit(abc, 'a')
        )

        with self.assertRaises(KeyError):
            pluckit(abc, 'values')

        self.assertEqual(
            3,
            pluckit(abc, len)
        )

        # dict keys can be ints
        moreData = { 0: 'a', 3: 'c' }
        self.assertEqual([ int, int ], list(map(type, moreData.keys())))
        self.assertEqual(
            'a',
            pluckit(moreData, 0)
        )


    def test_set(self):
        data = set([ 1, 2, 3 ])

        self.assertEqual(
            3,
            pluckit(data, len)
        )

        self.assertEqual(
            6,
            pluckit(data, lambda x: sum(x))
        )

        self.assertEqual(
            1,
            pluckit(data, 'pop')
        )


    def test_obj(self):
        class Foo():
            def foo(self):
                return 'foo'

            @classmethod
            def bar(cls):
                return 'bar'

            @staticmethod
            def baz():
                return 'baz'

            @property
            def prop(self):
                return 'abc'

            CONST = 123


        self.assertEqual(
            'foo',
            pluckit(Foo(), 'foo')
        )

        self.assertEqual(
            'bar',
            pluckit(Foo, 'bar')
        )
        self.assertEqual(
            'bar',
            pluckit(Foo(), 'bar')
        )

        self.assertEqual(
            'baz',
            pluckit(Foo, 'baz')
        )
        self.assertEqual(
            'baz',
            pluckit(Foo(), 'baz')
        )

        self.assertEqual(
            'abc',
            pluckit(Foo(), 'prop')
        )

        self.assertEqual(
            123,
            pluckit(Foo, 'CONST')
        )

        self.assertEqual(
            'Foo',
            pluckit(Foo, '__name__')
        )


    def test_tuple(self):
        data = (1, 2, 3)

        self.assertEqual(1, pluckit(data, 0))
        self.assertEqual(3, pluckit(data, len))


    def test_none(self):
        self.assertEqual(None, pluckit(None, 'abc'))
        self.assertEqual(None, pluckit(None, 123))
        self.assertEqual(None, pluckit(None, str))

        def explode():
            raise Exception('this should never execute')
        self.assertEqual(None, pluckit(None, explode))



if __name__ == '__main__':
    unittest.main()
