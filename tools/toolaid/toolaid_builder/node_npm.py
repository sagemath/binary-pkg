"""
Install stuff using Node + npm
"""

import os
import subprocess

import logging
log = logging.getLogger()


class NodeNpmBuilder(object):

    def __init__(self, config):
        self._config = config

    @property
    def config(self):
        return self._config
        
    @property
    def npm_path(self):
        return os.path.join(self.config.target_directory, 'bin', 'npm')

    @property
    def env(self):
        target = self.config.target_directory
        env = dict(os.environ)
        env.pop('MAKE', None)
        env['PATH'] = os.path.join(target, 'bin') + os.path.pathsep + env['PATH']
        env['PKG_CONFIG_PATH'] = os.path.join(target, 'lib/pkgconfig')
        return env
    
    def run(self):
        cmd = [
            self.npm_path,
            'install',
            '--global',
            '--prefix={0}'.format(self.config.target_directory),
        ]
        try:
            node_npm = self.config.yaml['node-npm']
        except KeyError:
            log.debug('no node npm packages specified, skipping')
            return
        for package, version in node_npm.items():
            if version is None:
                cmd.append(package)
            else:
                cmd.append('{0}@{1}'.format(package, version))
        log.debug('Executing ' + ' '.join(cmd))
        subprocess.check_call(cmd, env=self.env)
        


def build_node_npm(config):
    builder = NodeNpmBuilder(config)
    builder.run()


