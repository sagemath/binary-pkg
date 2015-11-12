


import re
import os
import unittest
from binary_pkg.file_filter import FileFilter



class TestFileFilter(unittest.TestCase):

    DATA = os.path.join(os.path.dirname(__file__), 'data')
    
    def test_file_filter(self):
        ff = FileFilter(self.DATA)
        ff.include('**')
        ff.exclude('**/*ignore')
        ff.include('**/*want')
        self.assertEqual(
            ff.sorted(),
            [os.path.join(self.DATA, 'a/a_want'), os.path.join(self.DATA, 'a/b/b_want'),
             os.path.join(self.DATA, 'root_ignore'), os.path.join(self.DATA, 'root_want')]
        )
