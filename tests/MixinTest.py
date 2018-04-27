#!/usr/bin/python

import os
import sys
import unittest

from collections import defaultdict

sys.path = [ os.path.abspath(os.path.join(os.path.dirname(__file__), '..')) ] + sys.path
from pluckit.pluckable import Pluckable


class MixinTest(unittest.TestCase):
    def test_list(self):
        class MyList(list, Pluckable):
            def __init__(self, val): self.val = val

        data = MyList(123)
        data += [1, 2, 3]

        self.assertEquals(
            [1, 2, 3],
            data
        )
        self.assertEquals(
            MyList,
            type(data)
        )
        self.assertEquals(123, data.val)

        res = data.pluck(str)
        self.assertEquals(['1', '2', '3'], res)
        self.assertEquals(MyList, type(res))
        self.assertEquals(123, res.val)


    def test_dict(self):
        class PDDict(defaultdict, Pluckable): pass
        data = PDDict(lambda: 123)

        self.assertEquals(
            123,
            data['zzz']
        )

        data.clear()
        data.update({
            'a': 1,
            'b': 2,
            'c': 3,
        })

        res = data.pluck(str)

        self.assertEquals(
            {
                'a' : '1',
                'b' : '2',
                'c' : '3',
            },
            res
        )

        # type is preserved
        self.assertEquals(PDDict, type(res))

        # default value is preserved
        self.assertEquals(123, data['zzz'])


    def test_set(self):
        class MySet(set, Pluckable):
            def __init__(self, val): self.val = val

        data = MySet(123)
        data.update({1, 2, 3})

        self.assertEquals(123, data.val)

        res = data.pluck(str)

        self.assertEquals({'1', '2', '3'}, res)

        # type is preserved
        self.assertEquals(MySet, type(res))

        # attribute is preserved
        self.assertEquals(123, res.val)


if __name__ == '__main__':
    unittest.main()
