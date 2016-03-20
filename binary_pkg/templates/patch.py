

class FileABC(object):

    def __init__(self, search_and_replace, filename):
        self.search = search_and_replace.search
        self.replace = search_and_replace.replace
        self.filename = filename
        self.st = os.stat(filename)

    def save(self):
        """
        Preserve timestamps
        """
        os.utime(self.filename, (self.st.st_atime, self.st.st_mtime))

        
class FileBinaryPatch(FileABC):

    def __init__(self, search_and_replace, filename):
        super(FileBinaryPatch, self).__init__(search_and_replace, filename)
        self.fh = open(filename, "r+b")
        
    def patch(self, start, end):
        """
        Perfom substitution in a fixed-size region of the file

        The file length is unchanged; If necessary the region is zero
        padded.

        Args:
            start(int): The start position of the string to replace
            end(int): The position of the terminating null
        """
        self.fh.seek(start)
        region = self.fh.read(end - start + 1)
        assert region[-1] == b'\0'
        substituted = region.replace(self.search, self.replace)
        substituted+= b'\0' * (end - start - len(substituted))
        self.fh.seek(start)
        self.fh.write(substituted)
        return self

    def save(self):
        self.fh.close()
        super(FileBinaryPatch, self).save()


class FileTextSearchReplace(FileABC):

    def __init__(self, search_and_replace, filename):
        super(FileTextSearchReplace, self).__init__(search_and_replace, filename)
        with open(self.filename, 'rb') as f:
            self.content = f.read()
        
    def substitute(self):
        """
        Perform the string substitution, changing the file length
        """
        self.content = self.content.replace(self.search, self.replace)
        return self
        
    def save(self):
        with open(self.filename, 'wb') as f:
            f.write(self.content)        
        super(FileTextSearchReplace, self).save()


class FileProxy(object):

    def __init__(self, search_and_replace, filename):
        self.search_and_replace = search_and_replace
        self.filename = filename

    def substitute(self):
        return FileTextSearchReplace(
            self.search_and_replace, self.filename
        ).substitute()
        
    def patch(self, start, end):
        return FileBinaryPatch(
            self.search_and_replace, self.filename
        ).patch(start, end)

        
class SearchAndReplace(object):

    def __init__(self, root_path, search, replace):
        self.root_path = root_path.encode('utf-8')
        self.search = search.encode('utf-8')
        self.replace = replace.encode('utf-8')
        if len(self.search) < len(self.replace):
            raise RuntimeError(
                'path can be at most {0} characters long, but {1} has {2} characters'.format(
                    len(self.search), self.replace, len(self.replace)))

    def __call__(self, filename):
        filename = os.path.join(self.root_path, filename)
        print('patching {0}'.format(filename))
        return FileProxy(self, filename)
