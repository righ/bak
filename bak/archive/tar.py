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
            def is_within_directory(directory, target):
                
                abs_directory = os.path.abspath(directory)
                abs_target = os.path.abspath(target)
            
                prefix = os.path.commonprefix([abs_directory, abs_target])
                
                return prefix == abs_directory
            
            def safe_extract(tar, path=".", members=None, *, numeric_owner=False):
            
                for member in tar.getmembers():
                    member_path = os.path.join(path, member.name)
                    if not is_within_directory(path, member_path):
                        raise Exception("Attempted Path Traversal in Tar File")
            
                tar.extractall(path, members, numeric_owner=numeric_owner) 
                
            
            safe_extract(tar, os.path.dirname(realpath), members=tar.getmembers())


class TBZArchiver(TarArchiver):
    """tar archiver that compressed by bz2
    """
    extension = 'tbz'
    mode = 'bz2'


class TGZArchiver(TarArchiver):
    """tar archiver that compressed by gzip
    [Deprecated]gzip(tgz) binary contains timestamp automatically,
    and even the same content, each different binary from being generated.
    """
    extension = 'tgz'
    mode = 'gz'
