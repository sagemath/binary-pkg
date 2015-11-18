

import platform


def osname():
    distname, version, extra = platform.linux_distribution()
    if distname:
        return '{0}_{1}'.format(distname, version)
    osx_version, empty, arch = platform.mac_ver()
    if osx_version:
        return 'OSX_{0}'.format(osx_version)
    raise RuntimeError('unknown distribution / os')
        

def arch():
    return platform.machine()



if __name__ == '__main__':
    print('OS name = "{0}"'.format(osname()))
    print('Architecture = "{0}"'.format(arch()))
    
    
