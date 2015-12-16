
class FilePatch(object):

    def __init__(self, search_and_replace, filename):
        self.search = search_and_replace.search
        self.replace = search_and_replace.replace
        self.filename = filename
        self.st = os.stat(filename)
        with open(self.filename, 'rb') as f:
            self.content = f.read()

    def substitute(self):
        """
        Perform the string substitution, changing the file length
        """
        self.content = self.content.replace(self.search, self.replace)
        return self
        
    def patch(self, start, end):
        """
        Perfom substitution in a fixed-size region of the file

        The file length is unchanged; If necessary the region is zero
        padded.

        Args:
            start(int): The start position of the string to replace
            end(int): The position of the terminating null
        """
        assert self.content[end:end+1] == b'\0'
        region = self.content[start:end]
        substituted = region.replace(self.search, self.replace)
        substituted+= b'\0' * (end - start - len(substituted))
        self.content = self.content[:start] + substituted + self.content[end:]
        return self

    def save(self):
        with open(self.filename, 'wb') as f:
            f.write(self.content)
        os.utime(self.filename, (self.st.st_atime, self.st.st_mtime))

        
        
class SearchAndReplace(object):

    def __init__(self, search, replace):
        self.search = search.encode('utf-8')
        self.replace = replace.encode('utf-8')
        if len(self.search) < len(self.replace):
            raise RuntimeError(
                'path can be at most {0} characters long, but {1} has {2} characters'.format(
                    len(self.search), self.replace, len(self.replace)))

    def __call__(self, filename):
        filename = os.path.join(self.replace, filename)
        print('patching {0}'.format(filename))
        return FilePatch(self, filename)
    


        
        
