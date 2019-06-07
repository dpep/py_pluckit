#!/usr/bin/env python

import os
import sys
import unittest

sys.path = [ os.path.abspath(os.path.join(os.path.dirname(__file__), '..')) ] + sys.path
from pluckit.pluckit import pluckit, path_regex



class PluckPathTest(unittest.TestCase):
    def test_path_regex(self):
        def match_path(expected, path):
            steps = []

            while path:
                match = path_regex.match(path)
                self.assertTrue(match)

                handle = match.group('handle') or match.group('subscript')
                steps.append(handle)
                path = path[len(match.group()):]
            self.assertEqual(expected, steps)

        match_path([ 'a' ], 'a')
        match_path([ 'a' ], '[a]')
        match_path([ '"a"' ], '["a"]')
        match_path([ "'a'" ], "['a']")
        match_path([ '0' ], '0')

        match_path([ 'a', 'b' ], 'a.b')
        match_path([ 'a', '0' ], 'a.0')

        match_path([ '*' ], '*')
        match_path([ '*' ], '[*]')
        match_path([ 'a', '*' ], 'a.*')
        match_path([ 'a', '*' ], 'a[*]')
        match_path([ '*', 'a' ], '*.a')


    def test_path_errors(self):
        def bad_path(path):
            self.assertFalse(path_regex.match(path))

        bad_path('')

        bad_path('.')
        bad_path('[]')

        bad_path('[')
        bad_path(']')
        bad_path('.[')
        bad_path('.]')

        bad_path('..')
        bad_path('.[]')
        bad_path('.[a]')
        bad_path('.[0]')

        with self.assertRaises(ValueError):
            pluckit([ 0 ], '0.')

        with self.assertRaises(ValueError):
            pluckit([], '*.')

        with self.assertRaises(ValueError):
            pluckit([], '[')

        with self.assertRaises(ValueError):
            pluckit([], '*[')


    def test_basic(self):
        data = [ [ 1, 2 ], [ 3 ], 4 ]

        self.assertEqual(1, pluckit(data, '0[0]'))
        self.assertEqual(2, pluckit(data, '0[1]'))
        self.assertEqual(3, pluckit(data, '1[0]'))

        self.assertEqual(4, pluckit(data, '-1'))
        self.assertEqual(2, pluckit(data, '0[-1]'))


        data = { 'a': { 'b': 1 }, 'c': { 'd': 1 } }
        self.assertEqual(1, pluckit(data, 'a["b"]'))
        self.assertEqual(1, pluckit(data, "a['b']"))


    def test_fns(self):
        class Foo:
            def foo(self):
                return 'foo'

        data = { 'a': { 'b': 1 }, 'c': { 'd': Foo() } }

        self.assertEqual(
            [ 'a', 'c' ],
            list(pluckit(data, '.keys'))
        )

        self.assertEqual(
            [ 'b' ],
            list(pluckit(data, 'a.keys'))
        )

        self.assertEqual(
            [ 1 ],
            list(pluckit(data, 'a.values'))
        )

        self.assertEqual(
            'foo',
            pluckit(data, 'c[d].foo')
        )

        self.assertEqual(
            'Foo',
            pluckit(data, 'c[d].__class__.__name__')
        )


    def test_errors(self):
        data = { 'a': [] }

        with self.assertRaises(IndexError):
            pluckit(data, 'a[0]')

        with self.assertRaises(AttributeError):
            pluckit(data, 'a.0')

        with self.assertRaises(AttributeError):
            pluckit(data, 'a.z')

        with self.assertRaises(KeyError):
            pluckit(data, 'z')

        with self.assertRaises(AttributeError):
            pluckit(data, '.z')


    def test_empty_list(self):
        with self.assertRaises(IndexError):
            pluckit([], '0')
        with self.assertRaises(IndexError):
            pluckit([], '-1')
        with self.assertRaises(AttributeError):
            pluckit([], '.0')


    def test_empty_dict(self):
        with self.assertRaises(KeyError):
            pluckit({}, 'a')

        with self.assertRaises(KeyError):
            pluckit({}, '0')


    def test_wildcard(self):
        data = [ [ 1 ], [ 2 ] ]
        self.assertEqual(data, pluckit(data, '*'))
        self.assertEqual(data, pluckit(data, '.*'))

        self.assertEqual(data, pluckit(data, '*.*'))
        self.assertEqual(data, pluckit(data, '*[*]'))
        self.assertEqual(data, pluckit(data, '.*.*'))

        self.assertEqual([ 1, 2 ], pluckit(data, '*[0]'))


        data = { 'a': { 'b': 1 } }
        self.assertEqual([{ 'b': 1 }], pluckit(data, '*'))
        self.assertEqual([{ 'b': 1 }], pluckit(data, '.*'))

        self.assertEqual([ 1 ], pluckit(data, '*[b]'))
        self.assertEqual([ 1 ], pluckit(data, 'a[*]'))

        self.assertEqual([ [ 1 ] ], pluckit(data, '*[*]'))
        self.assertEqual([ [ 1 ] ], pluckit(data, '*.*'))


    def test_wildcard_advanced(self):
        data = {
            'a': { 'k': 1, 'v': [ 1, 2 ] },
            'b': { 'k': 2, 'v': [ 3, 4 ] },
        }

        self.assertEqual(
            [ 1, 2 ],
            pluckit(data, '*[k]')
        )

        self.assertEqual(
            [ [ 1, 2 ], [ 3, 4 ] ],
            pluckit(data, '*[v]')
        )

        self.assertEqual(
            [ [ 1, 2 ], [ 3, 4 ] ],
            pluckit(data, '*[v]*')
        )

        self.assertEqual(
            [ 1, 3 ],
            pluckit(data, '*[v][0]')
        )


    def test_wildcard_empty(self):
        self.assertEqual([], pluckit([], '*'))
        self.assertEqual([], pluckit({}, '*'))

        self.assertEqual([], pluckit([], '*.*'))
        self.assertEqual([], pluckit({}, '*.*'))

        self.assertEqual([], pluckit([], '*.a'))


    def test_wildcard_errors(self):
        data = { 'a': [], 'b': 2 }

        with self.assertRaises(KeyError):
            pluckit(data, '["*"]')

        with self.assertRaises(TypeError):
            pluckit(data, 'a["*"]')

        with self.assertRaises(TypeError):
            pluckit(data, 'b.*')

        with self.assertRaises(ValueError):
            pluckit(data, '*.')


    def test_slice(self):
        data = [ 0, 1, 2, 3 ]

        self.assertEqual(
            data[1:3], # [ 1, 2 ]
            pluckit(data, '[1:3]')
        )

        self.assertEqual(
            data[2:],
            pluckit(data, '[2:]')
        )

        self.assertEqual(
            data[:2],
            pluckit(data, '[:2]')
        )

        self.assertEqual(
            data[::2],
            pluckit(data, '[::2]')
        )

        self.assertEqual(
            data[:],
            pluckit(data, '[:]')
        )

        self.assertEqual(
            data[::],
            pluckit(data, '[::]')
        )



if __name__ == '__main__':
    unittest.main()
