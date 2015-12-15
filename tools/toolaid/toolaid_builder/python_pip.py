"""
Install stuff using Python pip
"""

import os
import subprocess

import logging
log = logging.getLogger()


class PythonPipBuilder(object):

    def __init__(self, config):
        self._config = config

    @property
    def config(self):
        return self._config
        
    @property
    def pip_path(self):
        pip = os.path.join(self.config.target_directory, 'bin', 'pip')
        if os.path.exists(pip):
            return pip
        # Python 3.4+ bundles pip3
        pip3 = os.path.join(self.config.target_directory, 'bin', 'pip3')
        if os.path.exists(pip3):
            return pip3
        raise RuntimeError('pip is not installed at {0}'.format(
            os.path.join(self.config.target_directory, 'bin')))

    @property
    def env(self):
        target = self.config.target_directory
        env = dict(os.environ)
        env['PATH'] = os.path.join(target, 'bin') + os.path.pathsep + env['PATH']
        env['PKG_CONFIG_PATH'] = os.path.join(target, 'lib/pkgconfig')
        return env

    def run(self):
        cmd = [
            self.pip_path,
            'install',
        ]
        try:
            python_pip = self.config.yaml['python-pip']
        except KeyError:
            log.debug('no Python pip packages specified, skipping')
            return
        for key, value in python_pip.items():
            if value is None:
                cmd.append(key)
            else:
                cmd.append(key + value)
        log.debug('Executing ' + ' '.join(cmd))
        subprocess.check_call(cmd, env=self.env)
        


def build_python_pip(config):
    builder = PythonPipBuilder(config)
    builder.run()


