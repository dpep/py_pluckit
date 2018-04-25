#!/usr/bin/python

import os
import sys
import unittest

sys.path = [ os.path.abspath(os.path.join(os.path.dirname(__file__), '..')) ] + sys.path
from pluckit import pluckit, Pluckable


class PluckableTest(unittest.TestCase):
    def test_list(self):
        class PList(list, Pluckable): pass

        data = PList([ 0, 1, 2, 3 ])

        self.assertEquals(
            3,
            data.pluck(3),
        )

        self.assertEquals(
            4,
            data.pluck(len)
        )

        self.assertEquals(
            6,  # 0 + 1 + 2 + 3
            data.pluck(lambda x: sum(x))
        )

        self.assertEquals(
            [ 2, 1 ],
            data.pluck(2, 1),
        )


    def test_dict(self):
        class PDict(dict, Pluckable): pass
        abc = PDict({ 'a' : 1, 'b' : 2, 'c' : 3 })

        self.assertEquals(
            1,
            pluckit(abc, 'a')
        )

        self.assertEquals(
            [ 1, 2 ],
            pluckit(abc, 'a', 'b')
        )


    def test_obj(self):
        class Foo(Pluckable):
            def foo(self):
                return 'foo'

            @classmethod
            def bar(cls):
                return 'bar'


        self.assertEquals(
            'foo',
            Foo().pluck('foo')
        )

        self.assertEquals(
            [ 'foo', 'bar' ],
            Foo().pluck('foo', 'bar')
        )



if __name__ == '__main__':
    unittest.main()
