
import os
import unittest
from binary_pkg.path_placeholder import LENGTH, make_path


class TestPathPlaceholder(unittest.TestCase):

    def test_length(self):
        path = make_path(os.path.expanduser('~'), 'build')
        self.assertTrue(os.path.isabs(path))
        self.assertEqual(len(path), LENGTH)
        self.assertIn('/build/', path)
        self.assertEqual(path, make_path(os.path.expanduser('~'), 'build'))
