# coding: utf-8

import os
import re
import shutil
import filecmp
import uuid

from datetime import datetime
from .archive.tar import TarArchiver

DATETIME_FORMAT = '%Y%m%d%H%M%S%f'


def gen_suffix():
    return '.' + datetime.now().strftime(DATETIME_FORMAT)


class Item(object):
    def __repr__(self):
        return '<{0}: {1}>'.format(self.basename, len(self.history)

    def __init__(
        self, path,
        savepath=None, wrap=None, archiver=TarArchiver,
        **options
    ):
        self.path = path.rstrip('/')
        self.savepath = savepath or os.path.dirname(path) or './'
        if wrap:
            self.savepath = os.path.join(self.savepath, wrap)

        self.basename = os.path.basename(path)

        if not os.path.exists(path):
            raise Exception()

        self.options = options
        self.archiver = archiver(**options)

        self.isdir = os.path.isdir(path)
        if self.isdir:
            self.remove = shutil.rmtree
        else:
            self.remove = os.remove

        for self.basename in reversed(path.split('/')):
            if self.basename:
                break
        else:
            # TODO: add message
            raise Exception()

    @property
    def history(self):
        return sorted([
            item for item in os.listdir(self.savepath)
            if item.startswith(self.basename + '.')
        ])

    def temporary(self):
        tmppath = os.path.join(self.savepath, self.basename + gen_suffix())

        if not os.path.exists(self.savepath):
            os.makedirs(self.savepath)

        self.archiver.compress(self.path, tmppath, isdir=self.isdir)
        try:
            nochange = filecmp.cmp(
                tmppath,
                os.path.join(self.savepath, self.history[1])
            )
        except IndexError:
            nochange = False

        return tmppath, nochange

    def save(self, nochange=False):
        tmppath, _nochange = self.temporary()
        if not nochange and _nochange:
            os.remove(tmppath)

    def restore(self, nochange=False, keep=False):
        history = self.history
        if not history:
            # TODO: add message
            raise Exception()

        tmppath, _nochange = self.temporary()
        if nochange or not _nochange:
            self.remove(self.path)
            archive = os.path.join(self.savepath, history[1])
            self.archiver.decompress(archive, self.path, isdir=self.isdir)
            os.remove(archive)

        else:
            keep = False

        if not keep:
            os.remove(tmppath)
