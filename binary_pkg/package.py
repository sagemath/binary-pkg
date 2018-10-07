
import os
import stat
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

    def _make_user_rw(self, filename):
        st = os.stat(filename)
        os.chmod(filename, st.st_mode | stat.S_IREAD | stat.S_IWRITE )
    
    def copy(self):
        shutil.copy2(self._src, self._dst)
        self._make_user_rw(self._dst)

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
                return
            yield start
            start += len(marker)   # cannot have overlapping markers

    def find_terminators(self, marker):
        """
        Find positions of marker in the file
        
        Returns:
            dict: the keys are the terminators (byte after the marker, see ``ALL_TERMINATORS``) and
            the corresponding value is a tuple of start indices. Lists the start indices of the
            marker with the given terminator.
        """
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
            # The rpath can be /foo:/marker:/usr/lib, for example in gp
            log.warn('Contains zero-terminated strings but marker is not: {0}'
                     .format(self._src))
            # Pretend that we found zero terminators, see :meth:`find_patch`
            result[b'\0'] = tuple()
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
                return
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
        """
        Return the source directory

        This is where the application was built
        """
        return self._config.source_path

    @property
    def staging(self):
        """
        Return the staging directory

        This is the directory containing the binaries that will be
        distributed, e.g. as tar.bz2 file.
        """
        return self._package_config.staging_path

    @property
    def root(self):
        return self._package_config.root_path

    @property
    def config(self):
        return self._config
    
    @property
    def package_config(self):
        return self._package_config

    def copy(self):
        """
        Copy files from source to staging
        
        Only files that are included by the configuration yaml file
        (in the ``files:`` section) are copied.

        * Symlinks are turned into relative symlinks
        * File modification times are preserved
        * File are searched for hardcoded paths and any matches are is recorded.
        * Directories are recreated, even if empty
        """
        shutil.rmtree(self.root, ignore_errors=True)
        mkdir_p(self.root)
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
                if not os.path.isabs(linkto):   # make linkto absolute path
                    linkto = os.path.join(os.path.dirname(src), linkto)
                relative_dir = os.path.relpath(
                    os.path.dirname(linkto),
                    os.path.dirname(src)
                )
                relative_file = os.path.join(relative_dir, os.path.basename(linkto))
                os.symlink(relative_file, dst)
            elif os.path.isdir(src):
                log.debug('Directory {0}'.format(relative))
                mkdir_p(dst)
                self.copy_mtime(src, dst)
            elif os.path.isfile(src):
                f = InstallFile(src, dst)
                f.copy()
                if self.package_config.rewrite_path_filter.match(relative) == True:
                    log.debug('Copying {0}, checking path'.format(relative))
                    patch = f.find_patch(marker)
                    if patch:
                        self._patch[relative] = patch
                else:
                    log.debug('Copying {0}, ignoring path'.format(relative))
                self.copy_mtime(src, dst)
            else:
                raise ValueError('{0} is not a file, symlink, or directory'.format(relative))
        self.print_patch_summary()
        return self

    def copy_mtime(self, src, dst):
        """
        Copy the file modification time using nanosecond granularity
        """
        st = os.stat(src)
        os.utime(dst, ns=(st.st_atime_ns, st.st_mtime_ns))
    
    def print_patch_summary(self):
        filenames = sorted(self._patch.keys())
        for filename in filenames:
            patch = self._patch[filename]
            print('- {0}: {1}'.format(filename, patch))
    
    def strip(self):
        """
        Strip the executables in the staging directory
        """
        log.critical('todo: strip')
        return self

    def relocate_script(self):
        """
        Return the relocate script as string
        """
        template = jinja2_env.get_template('relocate-once.py')
        return template.render(
            patches=self._patch,
            SearchReplacePatch=SearchReplacePatch,
            BinaryPatch=BinaryPatch,
            search_string=self.source,
            isinstance=isinstance,
        )
        
    def save_relocate_script(self):
        """
        Save the relocate script in the correct location
        """
        relocate_py = os.path.join(self.staging, self.config.name, 'relocate-once.py')
        with open(relocate_py, 'wb') as f:
            f.write(self.relocate_script().encode('utf-8'))
        os.chmod(relocate_py, 0o755)
        
