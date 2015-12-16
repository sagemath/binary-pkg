
import os
import tempfile
import subprocess

import logging
log = logging.getLogger()



class BashScript(object):

    def __init__(self, source_code, tmp_path, cwd=None):
        self._cwd = cwd
        fd, self._filename = tempfile.mkstemp(dir=tmp_path, suffix='.sh')
        os.close(fd)
        self._source_code = source_code
        with open(self._filename, 'wb') as f:
            f.write(self._source_code.encode('utf-8'))
            
    def __repr__(self):
        return self._source_code
            
    def run(self):
        try:
            subprocess.check_call(['bash', self._filename], cwd=self._cwd)
        except subprocess.CalledProcessError:
            log.error('Script failed:')
            log.error(self._source_code)
            raise
        
    def output(self):
        try:
            stdout = subprocess.check_output(['bash', self._filename], cwd=self._cwd)
        except subprocess.CalledProcessError:
            log.error('Script failed:')
            log.error(self._source_code)
            raise
        return stdout.strip().decode('utf-8')
