
import os
import shutil
import re
import string

import logging
log = logging.getLogger()

from binary_pkg.file_util import mkdir_p
from binary_pkg.file_header import FileHeader
from binary_pkg.jinja2_env import jinja2_env


PATH_CHARS = (
    string.ascii_letters + string.digits + '!#$%&\()*+,-./;<=>?@[]^_{|}~'
).encode('ascii')

BINARY_PATH_TERMINATORS = b'\0'

TEXT_PATH_TERMINATORS = (
    ' \n\r\t:\'\"`'
).encode('ascii')

ALL_TERMINATORS = BINARY_PATH_TERMINATORS + TEXT_PATH_TERMINATORS

        
class SearchReplacePatch(object):

    def __init__(self):
        pass

    def __repr__(self):
        return "search&replace"
    

class BinaryPatch(object):

    def __init__(self, start, end):
        self.start = start
        self.end = end

    def __repr__(self):
        return "[{0},{1})".format(self.start, self.end)
    

class InstallFile(object):

    def __init__(self, src, dst):
        self._src = src
        self._dst = dst
        self._header = FileHeader(src)
        self._is_binary = None
        self._content = None
        self._has_zero = None

    def is_binary(self):
        if self._is_binary is None:
            self._is_binary = self._header.is_binary()
        return self._is_binary

    def has_zero(self):
        if self._has_zero is None:
            self._has_zero = b'\0' in self.content()
        return self._has_zero
    
    def copy(self):
        shutil.copy2(self._src, self._dst)

    def content(self):
        if self._content is None:
            with open(self._src, 'rb') as f:
                self._content = f.read()
        return self._content
        
    def find(self, marker):
        content = self.content()
        start = 0
        while True:
            start = content.find(marker, start)
            if start == -1:
                raise StopIteration
            yield start
            start += len(marker)   # cannot have overlapping markers

    def find_terminators(self, marker):
        result = dict()
        binary_terminator = False
        text_terminator = False
        for start in self.find(marker):
            term = self._find_terminator(marker, start, ALL_TERMINATORS)
            result[term] = result.get(term, ()) + (start,)
            if term is None:
                continue
            binary_terminator = binary_terminator or (term in BINARY_PATH_TERMINATORS)
            text_terminator = text_terminator or (term in TEXT_PATH_TERMINATORS)
        if self.is_binary() and text_terminator and not binary_terminator:
            log.warn('Suspicious text terminators {0} in {1}'.format(
                list(result.keys()), self._src))
        if not self.is_binary() and not self.has_zero() and binary_terminator:
            log.warn('Suspicious binary terminators {0} in {1}'.format(
                list(result.keys()), self._src))
        if self.has_zero() and text_terminator and not binary_terminator:
            log.critical('Contains zero-terminated strings but marker is not, ignoring: {0}'
                         .format(self._src))
            return dict()
        return result
            
    def _find_terminator(self, marker, start, terminators):
        content = self.content()
        end = start + len(marker)
        assert content[start:end] == marker
        pos = end
        while pos < len(content):
            ch = content[pos:pos+1]
            # print(pos, ch)
            if ch not in PATH_CHARS:
                if ch not in terminators:
                    log.error('At {0}'.format(content[start:pos+1]))
                    log.error('path terminator {0} not allowed in {1}'.format(ch, self._src))
                    raise SystemExit('invalid string terminator')
                # print('terminator')
                return ch
            pos += 1
        return None
        
    def find_zero_terminated(self, marker):
        """
        Returns pairs (start, end) of zero-terminated strings to search& replace
        """
        content = self.content()
        start = 0
        while True:
            start = content.find(marker, start)
            if start == -1:
                raise StopIteration
            end = start + len(marker)
            while end < len(content) and content[end:end+1] != b'\0':
                end += 1
            yield (start, end)
            start = end+1

    def find_patch(self, marker):
        occurences = self.find_terminators(marker)
        if not occurences:
            return
        if b'\0' in occurences.keys():
            return [BinaryPatch(start, end)
                    for start, end in self.find_zero_terminated(marker)]
        else:
            return SearchReplacePatch()

      
            

class Packager(object):

    def __init__(self, config, package_config):
        self._config = config
        self._package_config = package_config
        self._patch = dict()

    @property
    def source(self):
        return self._config.source_path

    @property
    def staging(self):
        return self._package_config.staging_path

    @property
    def config(self):
        return self._config
    
    @property
    def package_config(self):
        return self._package_config

    def copy(self):
        shutil.rmtree(os.path.join(self.staging, self.config.name), ignore_errors=True)
        marker = self.source.encode('utf-8')
        for src in self.package_config.files():
            assert src.startswith(self.source)
            relative = src[len(self.source)+1:]
            assert not os.path.isabs(relative)
            dst = os.path.join(self.staging, self.config.name, relative)
            if os.path.islink(src):
                log.debug('Symlink {0}'.format(relative))
                mkdir_p(os.path.dirname(dst))
                linkto = os.readlink(src)
                os.symlink(linkto, dst)
            elif os.path.isdir(src):
                log.debug('Directory {0}'.format(relative))
                mkdir_p(os.path.dirname(dst))
            elif os.path.isfile(src):
                log.debug('Copying {0}'.format(relative))
                f = InstallFile(src, dst)
                f.copy()
                patch = f.find_patch(marker)
                if patch:
                    self._patch[relative] = patch
            else:
                assert False, 'special file'
        self.print_patch_summary()
        return self
    
    def print_patch_summary(self):
        filenames = sorted(self._patch.keys())
        for filename in filenames:
            patch = self._patch[filename]
            print('- {0}: {1}'.format(filename, patch))
    
    
    def strip(self):
        log.critical('todo: strip')
        return self

    def install_script(self):
        template = jinja2_env.get_template('install.py')
        return template.render(
            patches=self._patch,
            SearchReplacePatch=SearchReplacePatch,
            BinaryPatch=BinaryPatch,
            search_string=self.source,
            isinstance=isinstance,
        )
        
    def save_install_script(self):
        install_py = os.path.join(self.staging, self.config.name, 'install.py')
        with open(install_py, 'wb') as f:
            f.write(self.install_script().encode('utf-8'))
        os.chmod(install_py, 0o755)
        
