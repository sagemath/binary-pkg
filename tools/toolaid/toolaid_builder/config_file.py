import os
import yaml


class ConfigurationFile(object):

    def __init__(self, filename):
        self._filename = os.path.abspath(filename)
        with open(self.filename, 'rb') as f:
            self._yaml = yaml.load(f)

    @property
    def filename(self):
        """
        The full qualified name of the source yaml file
        """
        return self._filename

    @property
    def target_directory(self):
        """
        Full qualified name of the target directory
        """
        return os.path.splitext(self.filename)[0]

    @property
    def name(self):
        """
        The name of the configuration file

        This is just the basename of the yaml file, excluding the
        extension. For example, ``/foo/bar.yaml`` has name ``bar``
        """
        return os.path.basename(self.target_directory)

    @property
    def yaml(self):
        return self._yaml

    
    
        
