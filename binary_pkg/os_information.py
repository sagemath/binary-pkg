

import platform
import ld
import string


def filename_sanitize(s):
    """
    Sanitize the string so that it can be used as a part of a filename
    """
    allowed = string.ascii_letters + string.digits + '._-'
    def escape(ch):
        return ch if ch in allowed else '_'
    return ''.join([escape(ch) for ch in s])


def osname():
    distname, version, extra = ld.linux_distribution()
    if distname:
        return filename_sanitize('{0}_{1}'.format(distname, version))
    osx_version, empty, arch = platform.mac_ver()
    if osx_version:
        return filename_sanitize('OSX_{0}'.format(osx_version))
    raise RuntimeError('unknown distribution / os')
        

def arch():
    return filename_sanitize(platform.machine())



if __name__ == '__main__':
    print('OS name = "{0}"'.format(osname()))
    print('Architecture = "{0}"'.format(arch()))
    
    
