
import sys
import os
import yaml
import subprocess


def identify_platform_config():
    if sys.platform == 'darwin':
        return 'darwin.yaml'
    elif sys.platform == 'linux':
        return 'centos.yaml'
    else:
        raise NotImplementedError('unknown platform: {0}'.format(sys.platform))

    
class HashstackBuilder(object):

    def __init__(self, platform, config):
        self._platform = platform
        self._config = config

    @property
    def config(self):
        return self._config
        
    @property
    def default_yaml(self):
        return os.path.join(self.hashstack_path, 'default.yaml')

    @property
    def hit_path(self):
        toolaid = os.path.dirname(os.path.dirname(__file__))
        return os.path.join(toolaid, 'bootstrap-files', 'hashdist', 'bin', 'hit')
    
    @property
    def hashstack_path(self):
        toolaid = os.path.dirname(os.path.dirname(__file__))
        return os.path.join(toolaid, 'bootstrap-files', 'hashstack')

    def to_dict(self):
        result = dict(self.config.yaml['hashstack'])
        result['extends'] = [
            dict(file=self._platform)
        ]
        return result
        
    def __repr__(self):
        return yaml.dump(self.to_dict())

    def _write_default_yaml(self):
        with open(self.default_yaml, 'wt') as f:
            f.write(yaml.dump(self.to_dict()))
        
    def hit_develop(self):
        self._write_default_yaml()
        subprocess.check_call([
            self.hit_path,
            'develop', '-j8', '-f',
            self.default_yaml,
            self.config.target_directory,
        ])
            
    

    
def build_hashstack(config):
    platform = identify_platform_config()
    default = HashstackBuilder(platform, config)
    default.hit_develop()
