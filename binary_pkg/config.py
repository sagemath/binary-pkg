
import os
import yaml
import multiprocessing
import string
import textwrap

from binary_pkg.path_placeholder import make_path
from binary_pkg.bash_script import BashScript
from binary_pkg.file_util import mkdir_p
from binary_pkg.os_information import osname, arch
from binary_pkg.file_filter import FileFilter


def filename_escape(name):
    def escape(ch):
        if ch in string.ascii_letters + string.digits:
            return ch
        else:
            return '_'
    return ''.join(map(escape, name))



class ConfigurationError(Exception):
    pass


class PackageConfiguration(object):

    def __init__(self, config, data):
        self._config = config
        self._data = data
        self._files = None
        self._rewrite_path_filter = None

    @property
    def name(self):
        return self._data['name']
        
    @property
    def staging_path(self):
        name = filename_escape(self.name)
        path = os.path.join(self._config.root_path, 'staging', name)
        mkdir_p(path)
        return path

    @property
    def root_path(self):
        return os.path.join(self.staging_path, filename_escape(self._config.name))
    
    def _expand_package_script(self, template):
        return template.format(
            version=self._config.version,
            osname=osname(),
            arch=arch(),
            path=filename_escape(self._config.name),
            dist=self._config.dist_path,
        )
            
    @property
    def dist_script(self):
        script = self._expand_package_script(self._data['command'])
        return BashScript(script, self._config.tmp_path, cwd=self.staging_path)
    
    def files(self):
        if self._files is not None:
            return self._files
        ff = FileFilter(self._config.source_path)
        selectors = self._data.get('files', [])
        for selector in selectors:
            if list(selector.keys()) == ['include']:
                ff.include(selector['include'])
            elif list(selector.keys()) == ['exclude']:
                ff.exclude(selector['exclude'])
            else:
                raise ConfigurationError('file selector must be include xor exclude')
        self._files = ff.sorted()
        return self._files

    @property
    def rewrite_path_filter(self):
        if self._rewrite_path_filter is not None:
            return self._rewrite_path_filter
        ff = FileFilter(self._config.source_path)
        selectors = self._data.get('files', []) + self._data.get('rewrite_path', [])
        for selector in selectors:
            if list(selector.keys()) == ['include']:
                ff.include(selector['include'])
            elif list(selector.keys()) == ['exclude']:
                ff.exclude(selector['exclude'])
            else:
                raise ConfigurationError('file selector must be include xor exclude')
        self._rewrite_path_filter = ff
        return self._rewrite_path_filter

class Configuration(object):

    def __init__(self, filename):
        self._filename = str(filename)
        with open(filename, 'r') as f:
            self._data = yaml.safe_load(f.read())
            
    @property
    def root_path(self):
        return os.path.dirname(os.path.abspath(self._filename))

    @property
    def dist_path(self):
        path = os.path.join(self.root_path, 'dist')
        mkdir_p(path)
        return path

    @property
    def source_path(self):
        path = make_path(self.root_path, 'source', filename_escape(self.name))
        mkdir_p(path)
        return path
    
    @property
    def tmp_path(self):
        path = os.path.join(self.root_path, 'tmp', filename_escape(self.name))
        mkdir_p(path)
        return path

    @property
    def name(self):
        return self._data['name']

    @property
    def repository(self):
        return self._data['repository']

    @property
    def branch(self):
        return self._data['branch']

    def _expand_build_script(self, template):
        return template.format(
            ncpu=multiprocessing.cpu_count()
        )

    @property
    def build_script(self):
        script = self._expand_build_script(self._data['build'])
        return BashScript(script, self.tmp_path, cwd=self.source_path)

    @property
    def package(self):
        return [PackageConfiguration(self, pkg_data) for pkg_data in self._data['package']]

    @property
    def version(self):
        return BashScript(self._data['version'], self.tmp_path, cwd=self.source_path).output()

    def __repr__(self):
        result = textwrap.dedent("""
        Packaging script for {self.name} version {self.version}

        Build script:
        {build_script}
        """).format(
            self=self,
            build_script=textwrap.indent(str(self.build_script), ' '*4)
        )

        for i, pkg in enumerate(self.package):
            result += textwrap.dedent("""
            Package #{i}: {pkg.name}
            {package_script}
            """).format(
                pkg=pkg,
                i=i, 
                package_script=textwrap.indent(str(pkg.package_script), ' '*4)
            )
            for f in pkg.files():
                result += f + '\n'
        return result
