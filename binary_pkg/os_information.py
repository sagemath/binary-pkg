# -*- coding: utf-8 -*-

from __future__ import (absolute_import, division, print_function, unicode_literals)

import platform
import ld
import string


def filename_sanitize(s):
    """
    Sanitize the string so that it can be used as a part of a filename.
    """
    allowed = string.ascii_letters + string.digits + '._-'
    def escape(ch):
        return ch if ch in allowed else '_'
    return ''.join([escape(ch) for ch in s])


def osname():
    """
    Return a string for the operating system name.
    """
    distname, version, extra = ld.linux_distribution()
    if distname:
        return filename_sanitize('{0}_{1}'.format(distname, version))
    macos_version, empty, arch = platform.mac_ver()
    if macos_version:
        return filename_sanitize('macOS_{0}'.format(macos_version))
    raise RuntimeError('unknown distribution / os')


def arch():
    """
    Return a string for the architecture (processor family).
    """
    return filename_sanitize(platform.machine())


if __name__ == '__main__':
    print('OS name = "{0}"'.format(osname()))
    print('Architecture = "{0}"'.format(arch()))
