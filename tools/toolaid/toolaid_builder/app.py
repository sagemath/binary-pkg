import os
import tempfile
import yaml
from toolaid_builder.gitignore import update_gitignore
from toolaid_builder.hashstack import build_hashstack
from toolaid_builder.python_pip import build_python_pip
from toolaid_builder.node_npm import build_node_npm
from toolaid_builder.ruby_gem import build_ruby_gem
from toolaid_builder.activate_script import write_activate_script

class Application(object):

    def __init__(self, repo_root):
        self._repo_root = repo_root
        update_gitignore(self.tools_root)

    @property
    def repo_root(self):
        return self._repo_root

    @property
    def tools_root(self):
        return os.path.join(self.repo_root, 'tools')
    
    def show(self, config):
        print('#' * 79)
        print('### Configuration file: ' + config.filename)
        print(yaml.dump(config.yaml))

    def build(self, config):
        build_hashstack(config)
        build_python_pip(config)
        build_ruby_gem(config)
        build_node_npm(config)
        os.symlink(
            os.path.relpath(config.filename, config.target_directory),
            os.path.join(config.target_directory, 'configuration.yaml')
        )
        write_activate_script(config)

    def build_pip(self, config):
        build_python_pip(config)

    def build_npm(self, config):
        build_node_npm(config)

    def build_gem(self, config):
        build_ruby_gem(config)
        
