
import unittest
from collections import namedtuple

from pluckit import pluck

Coordinate = namedtuple('Coordinate', ['x', 'y'])  # hashable


class SetTest(unittest.TestCase):
    def test_basic(self):
        data = {
            Coordinate(x=1, y=2),
            Coordinate(x=2, y=4),
            Coordinate(x=3, y=6),
        }

        self.assertEqual(
            {1, 2, 3},
            pluck(data, 'x')
        )



if __name__ == '__main__':
    unittest.main()
