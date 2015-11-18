
import re
import os
import unittest
from binary_pkg.os_information import osname, arch



class TestOsInformation(unittest.TestCase):

    def test_architecture(self):
        self.assertIn(arch(), [
            'x86_64', 'i386', 'i586', 'i686'
        ])

    def test_osname(self):
        self.assertIn(osname(), [
            'Fedora_23', 'OSX_10.11.1',
        ])
