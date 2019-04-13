#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Download file from the internet

Avoids dependency on curl/wget to download miniconda

Usage:

    download.py filename.ext http://url/to/file
"""
from __future__ import print_function

import sys
import logging

try:
    # Python 3
    import urllib.request as urllib
except ImportError:
    import urllib


logging.basicConfig()
log = logging.getLogger()


class ProgressBar(object):
    """
    Progress bar as urllib reporthook
    """

    def __init__(self, stream, length=70):
        self.length = length
        self.progress = 0
        self.stream = stream

    def start(self):
        self.stream.write('[')
        self.stream.flush()

    def __call__(self, chunks_so_far, chunk_size, total_size):
        if total_size == -1:  # we do not know size
            n = 0 if chunks_so_far == 0 else self.length // 2
        else:
            n = chunks_so_far * chunk_size * self.length // total_size
        if n > self.length: 
            # If there is a Content-Length, this will be sent as the last progress
            return
        # n ranges from 0 to length*total (exclude), so we'll print at most length dots
        if n >= self.progress:
            self.stream.write('.' * (n-self.progress))
            self.stream.flush()
        self.progress = n

    def stop(self):
        missing = '.' * (self.length - self.progress)
        self.stream.write(missing + ']\n')
        self.stream.flush()

    def error_stop(self):
        missing = 'x' * (self.length - self.progress)
        self.stream.write(missing + ']\n')
        self.stream.flush()


class DownloadError(IOError):
    pass


class Download(object):
    """
    Download HTTP URL
    
    INPUT:

    - ``url`` -- string. The URL to download.

    - ``destination`` -- string or ``None`` (default). The destination
      file name to save to. If not specified, the file is written to
      stdout.

    - ``progress`` -- boolean (default: ``True``). Whether to print a
      progress bar to stderr. For testing, this can also be a stream
      to which the progress bar is being sent.

    - ``ignore_errors`` -- boolean (default: ``False``). Catch network
      errors (a message is still being logged).
    """

    def __init__(self, url, destination=None, progress=True, ignore_errors=False):
        self.url = url
        self.destination = destination or '/dev/stdout'
        self.progress = (progress is not False)
        self.progress_stream = sys.stderr if isinstance(progress, bool) else progress
        self.ignore_errors = ignore_errors

    def http_error_default(self, url, fp, errcode, errmsg, headers):
        """
        Callback for the URLopener to raise an exception on HTTP errors
        """
        fp.close()
        raise DownloadError(errcode, errmsg, url)

    def start_progress_bar(self):
        if self.progress:
            self.progress_bar = ProgressBar(self.progress_stream)
            self.progress_bar.start()

    def success_progress_bar(self):
        if self.progress:
            self.progress_bar.stop()

    def error_progress_bar(self):
        if self.progress:
            self.progress_bar.error_stop()
    
    def run(self):
        opener = urllib.FancyURLopener()
        opener.http_error_default = self.http_error_default
        self.start_progress_bar()
        try:
            if self.progress:
                filename, info = opener.retrieve(
                    self.url, self.destination, self.progress_bar)
            else:
                filename, info = opener.retrieve(
                    self.url, self.destination)
        except IOError as err:
            self.error_progress_bar()
            log.error(err)
            if not self.ignore_errors:
                raise
        self.success_progress_bar()


if __name__ == '__main__':
    print(sys.argv)
    program_name, destination, url = sys.argv[:3]
    print('Downloading {} -> {}'.format(url, destination))
    dl = Download(url, destination=destination)
    dl.run()
