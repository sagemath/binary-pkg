

import os
from binary_pkg.globber import glob_to_regex

INCLUDE = 'include'
EXCLUDE = 'exclude'


class FileFilter(object):

    def __init__(self, path):
        self._path = path
        self._filters = []

    def include(self, pattern):
        regex = glob_to_regex(pattern)
        self._filters.append((INCLUDE, regex.match))
        
    def exclude(self, pattern):
        regex = glob_to_regex(pattern)
        self._filters.append((EXCLUDE, regex.match))

    def __repr__(self):
        return '\n'.join(self._files)

    def match(self, relative_path):
        assert not os.path.isabs(relative_path)
        for filter_type, matcher in reversed(self._filters):
            match = matcher(relative_path)
            if filter_type == INCLUDE and match:
                return True
            elif filter_type == EXCLUDE and match:
                return False
        return None
    
    def __iter__(self):
        start = len(self._path)
        for path, dirs, files in os.walk(self._path):
            for filename in dirs + files:
                fqn = os.path.join(path, filename)
                relative = fqn[start+1:]
                matches = self.match(relative)
                if matches == True:
                    yield fqn

    def sorted(self):
        return sorted(self)
                    
