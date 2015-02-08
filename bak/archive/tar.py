# coding: utf-8

import os
import tarfile
from .base import BaseArchiver


class TarArchiver(BaseArchiver):
    """tar archiver
    """
    extension = 'tar'
    mode = ''

    def compress(self, src, dst, isdir=True):
        """tar file compressor
        """
        extension = self.options.get('extension', True)
        if extension:
            if isinstance(extension, bool):
                extension = self.extension
            dst += '.' + extension

        with tarfile.open(dst, 'w:' + self.mode) as tar:
            tar.add(src.rstrip('/'), filter=self.options.get('archive_filter'))
        return dst

    def decompress(self, src, dst, isdir=True):
        """tar file decompressor
        """
        realpath = os.path.realpath(dst)
        with tarfile.open(src) as tar:
            tar.extractall(os.path.dirname(realpath), members=tar.getmembers())


class TBZArchiver(TarArchiver):
    """tar archiver that compressed by bz2
    """
    extension = 'tbz'
    mode = 'bz2'

'''
class TGZArchiver(TarArchiver):
    """tar archiver that compressed by gzip
    """
    extension = 'tgz'
    mode = 'gz'
'''
