#!/usr/bin/env python

import os
import sys
import unittest

sys.path = [ os.path.abspath(os.path.join(os.path.dirname(__file__), '..')) ] + sys.path
from pluckit.pluckit import pluckit


class PluckPathTest(unittest.TestCase):
    def test(self):
        data = { 'a': [ { 'v': 1 }, 2 ] }

        self.assertEqual(
            1,
            pluckit(data, 'a.0.v'),
        )

        self.assertEqual(
            1,
            pluckit(data, 'a[0][v]'),
        )

        self.assertEqual(
            1,
            pluckit(data, 'a[0]["v"]'),
        )


    def test_errors(self):
        data = { 'a': [] }

        with self.assertRaises(IndexError):
            pluckit(data, 'a[0]')

        with self.assertRaises(IndexError):
            pluckit(data, 'a.0')

        with self.assertRaises(TypeError):
            pluckit(data, 'a.z')

        with self.assertRaises(KeyError):
            pluckit(data, 'z')




if __name__ == '__main__':
    unittest.main()
