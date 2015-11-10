"""
Install stuff using Ruby gems
"""

import os
import subprocess

import logging
log = logging.getLogger()


class RubyGemBuilder(object):

    def __init__(self, config):
        self._config = config

    @property
    def config(self):
        return self._config
        
    @property
    def gem_path(self):
        return os.path.join(self.config.target_directory, 'bin', 'gem')

    @property
    def env(self):
        target = self.config.target_directory
        env = dict(os.environ)
        env['GEM_HOME'] = target
        env['PATH'] = os.path.join(target, 'bin') + os.path.pathsep + env['PATH']
        env['PKG_CONFIG_PATH'] = os.path.join(target, 'lib/pkgconfig')
        env['NOKOGIRI_USE_SYSTEM_LIBRARIES'] = '1'
        return env
    
    def run(self):
        cmd = [
            self.gem_path,
            'install',
        ]
        try:
            ruby_gem = self.config.yaml['ruby-gem']
        except KeyError:
            log.debug('no Ruby gem packages specified, skipping')
            return
        for gem, version in ruby_gem.items():
            if version is None:
                cmd.append(gem)
            else:
                cmd.append("{0}:{1}".format(gem, version))
        log.debug('Executing ' + ' '.join(cmd))
        subprocess.check_call(cmd, env=self.env)
        


def build_ruby_gem(config):
    builder = RubyGemBuilder(config)
    builder.run()


