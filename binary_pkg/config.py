
import os
import yaml
import multiprocessing
import string

from binary_pkg.path_placeholder import make_path
from binary_pkg.bash_script import BashScript
from binary_pkg.file_util import mkdir_p
from binary_pkg.os_information import osname, arch


class ConfigurationError(Exception):
    pass


class PackageConfiguration(object):

    def __init__(self, config, data):
        self._config = config
        self._data = data

    @property
    def name(self):
        return self._data['name']
        
    @property
    def staging_path(self):
        def escape(ch):
            if ch in string.ascii_letters + string.digits:
                return ch
            else:
                return '_'
        name = ''.join(map(escape, self.name))
        path = os.path.join(self._config.root_path, 'staging', name)
        mkdir_p(path)
        return path

    def _expand_package_script(self, template):
        return template.format(
            version=self._config.version,
            osname=osname(),
            arch=arch(),
            path=self.staging_path,
        )
            
    @property
    def package_script(self):
        script = self._expand_package_script(self._data['command'])
        return BashScript(script, self._config.tmp_path)
    


class Configuration(object):

    def __init__(self, filename):
        self._filename = str(filename)
        with open(filename, 'r') as f:
            self._data = yaml.safe_load(f.read())
            
    @property
    def root_path(self):
        return os.path.dirname(os.path.abspath(self._filename))

    @property
    def source_path(self):
        path = make_path(self.root_path, 'source', self.name)
        mkdir_p(path)
        return path
    
    @property
    def tmp_path(self):
        path = os.path.join(self.root_path, 'tmp', self.name)
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
        return BashScript(script, self.tmp_path)

    @property
    def package(self):
        return [PackageConfiguration(self, pkg_data) for pkg_data in self._data['package']]

    @property
    def version(self):
        return BashScript(self._data['version'], self.tmp_path).output(cwd=self.source_path)
