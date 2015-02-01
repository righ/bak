# coding: utf-8

import os
import tarfile
from .base import BaseArchiver

MAPPING = {
    'bz2': ('bz2', 'tbz', ),
    'tar': ('', 'tar')
}


class TarArchiver(BaseArchiver):
    """tar file manager
    """
    def compress(self, src, dst, isdir=True):
        """tar file compressor
        """
        method = self.options.get('method', 'bz2')
        try:
            mode, extension_default = MAPPING[method]
        except KeyError:
            # TODO: add message
            raise Exception()

        extension = self.options.get('extension', True)
        if extension:
            if isinstance(extension, bool):
                extension = extension_default
            dst += '.' + extension

        def exclude_filter(tarinfo):
            """exclusion rule
            """
            for exclude_rule in self.options.get('exclude_rules', ()):
                if exclude_rule.search(tarinfo.name):
                    return None
            return tarinfo

        with tarfile.open(dst, 'w:' + mode) as tar:
            tar.add(src.rstrip('/'), filter=exclude_filter)
        return dst

    def decompress(self, src, dst, isdir=True):
        """tar file decompressor
        """
        realpath = os.path.realpath(dst)
        with tarfile.open(src) as tar:
            tar.extractall(os.path.dirname(realpath), members=tar.getmembers())
