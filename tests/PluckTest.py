#!/usr/bin/python

import os
import sys
import unittest

sys.path = [ os.path.abspath(os.path.join(os.path.dirname(__file__), '..')) ] + sys.path
from pluckit.pluckit import pluckit


class PluckTest(unittest.TestCase):
    def test_list(self):
        data = [ 0, 1, 2, 3 ]

        self.assertEquals(
            3,
            pluckit(data, 3),
        )

        self.assertEquals(
            list,
            pluckit(data, '__class__'),
        )

        self.assertEquals(4, len(data))
        self.assertEquals(
            3,
            pluckit(data, 'pop'),
        )
        self.assertEquals(3, len(data))

        self.assertEquals(
            3,
            pluckit(data, len),
        )

        self.assertEquals(
            3,  # 0 + 1 + 2
            pluckit(data, lambda x: sum(x))
        )


    def test_dict(self):
        abc = { 'a' : 1, 'b' : 2, 'c' : 3 }

        self.assertEquals(
            1,
            pluckit(abc, 'a')
        )

        with self.assertRaises(KeyError):
            pluckit(abc, 'values')

        self.assertEquals(
            3,
            pluckit(abc, len)
        )


    def test_set(self):
        data = set([ 1, 2, 3 ])

        self.assertEquals(
            3,
            pluckit(data, len)
        )

        self.assertEquals(
            6,
            pluckit(data, lambda x: sum(x))
        )

        self.assertEquals(
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


        self.assertEquals(
            'foo',
            pluckit(Foo(), 'foo')
        )

        self.assertEquals(
            'bar',
            pluckit(Foo, 'bar')
        )
        self.assertEquals(
            'bar',
            pluckit(Foo(), 'bar')
        )

        self.assertEquals(
            'baz',
            pluckit(Foo, 'baz')
        )
        self.assertEquals(
            'baz',
            pluckit(Foo(), 'baz')
        )

        self.assertEquals(
            'abc',
            pluckit(Foo(), 'prop')
        )

        self.assertEquals(
            123,
            pluckit(Foo, 'CONST')
        )

        self.assertEquals(
            'Foo',
            pluckit(Foo, '__name__')
        )


    def test_none(self):
        self.assertEquals(None, pluckit(None, 'abc'))
        self.assertEquals(None, pluckit(None, 123))
        self.assertEquals(None, pluckit(None, str))

        def explode():
            raise Exception('this should never execute')
        self.assertEquals(None, pluckit(None, explode))



if __name__ == '__main__':
    unittest.main()
