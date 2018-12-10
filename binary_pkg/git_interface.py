# -*- coding: utf-8 -*-

from __future__ import (absolute_import, division, print_function, unicode_literals)

import os
import subprocess


def git_clone(config):
    if os.path.exists(os.path.join(config.source_path, '.git')):
        subprocess.check_call([
            'git', 'checkout', config.branch
        ], cwd=config.source_path)
        subprocess.check_call([
            'git', 'pull', '--ff-only'
        ], cwd=config.source_path)
    else:
        subprocess.check_call([
            'git', 'clone', config.repository, '-b', config.branch, config.source_path
        ])

