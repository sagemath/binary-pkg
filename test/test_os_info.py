
import re
import os
import unittest
from binary_pkg.os_information import osname, arch, filename_sanitize



class TestOsInformation(unittest.TestCase):

    def test_architecture(self):
        self.assertIn(arch(), [
            'x86_64', 'i386', 'i586', 'i686'
        ])

    def test_osname(self):
        self.assertIn(osname(), [
            'Fedora_23', 'OSX_10.11.3',
        ])

    def test_filename_sanitize(self):
        self.assertEqual(filename_sanitize('Fedora'), 'Fedora')
        self.assertEqual(filename_sanitize('23'), '23')
        self.assertEqual(filename_sanitize('debian'), 'debian')
        self.assertEqual(filename_sanitize('jesse/sid'), 'jesse_sid')
        
