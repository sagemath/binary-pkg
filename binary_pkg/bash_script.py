
import os
import tempfile
import subprocess



class BashScript(object):

    def __init__(self, source_code, tmp_path):
        fd, self._filename = tempfile.mkstemp(dir=tmp_path, suffix='.sh')
        os.close(fd)
        self._source_code = source_code
        with open(self._filename, 'wb') as f:
            f.write(self._source_code.encode('utf-8'))
            
    def __repr__(self):
        return self._source_code
            
    def run(self, cwd=None):
        subprocess.check_call(['bash', self._filename], cwd=cwd)
        
    def output(self, cwd=None):
        stdout = subprocess.check_output(['bash', self._filename], cwd=cwd)
        print(stdout)
        return stdout.strip()
