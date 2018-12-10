# -*- coding: utf-8 -*-

from __future__ import (absolute_import, division, print_function, unicode_literals)

import os
import unittest

from binary_pkg.bash_script import BashScript
from binary_pkg.config import Configuration
from binary_pkg.search_path import safe_search_path


HELLO_WORLD_SH = os.path.join(
    os.path.dirname(__file__), 'fixtures', 'hello_world.sh')

ECHO_PATH_SH = os.path.join(
    os.path.dirname(__file__), 'fixtures', 'echo_path.sh')

HELLO_WORLD_YAML = os.path.join(
    os.path.dirname(__file__), 'fixtures', 'hello_world.yaml')

TEST_YAML = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), 'test.yaml')


config = Configuration(HELLO_WORLD_YAML)


class TestBashScript(unittest.TestCase):

    def test_run_script(self):
        echo_path = BashScript(ECHO_PATH_SH, config.tmp_path)
        echo_path.run()

    def test_read_output(self):
        hello_world = BashScript(HELLO_WORLD_SH, config.tmp_path)
        self.assertEqual(hello_world.output(), 'Hello World')

    def test_build_script(self):
        output = config.build_script.output()
        hello, path = output.splitlines()
        self.assertEqual(hello, 'Hello World')

    def test_search_path(self):
        first = os.environ['PATH'].split(':')[0]
        assert(first not in safe_search_path(first))
        
    def test_scrub_path(self):
        tc = Configuration(TEST_YAML)
        self.assertNotIn(tc.root_path, tc._PATH)
        self.assertNotIn('binary-pkg', tc._PATH)
        
