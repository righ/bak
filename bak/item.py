# coding: utf-8

import os
import re
import shutil
import filecmp
import uuid

from datetime import datetime
from .archive.tar import TBZArchiver
from .exception import (
    ItemNotFound,
    ItemPathInvalid,
    HistoryEmpty,
)

DATETIME_FORMAT = '%Y%m%d%H%M%S%f'


class Item(object):
    def __repr__(self):
        return '<{0} ({1})>'.format(self.basename, len(self.history))

    def __init__(self, path, savepath=None, archiver=TBZArchiver, **options):
        self.path = path.rstrip('/')
        self.basename = os.path.basename(self.path)
        self.startswith = re.compile('^' + re.escape(self.basename) + '\.([0-9]{14,20})')

        abspath = os.path.realpath(path)
        if not os.path.exists(abspath):
            raise ItemNotFound(abspath)

        self.options = options
        self.archiver = archiver(**options)

        self.isdir = os.path.isdir(abspath)
        if self.isdir:
            self.remove = shutil.rmtree
        else:
            self.remove = os.remove

        for self.basename in reversed(abspath.split('/')):
            if self.basename:
                break
        else:
            raise ItemPathInvalid(abspath)

        # if no problem, make save dir
        self.savepath = savepath or os.path.dirname(self.path) or './'
        if not os.path.exists(self.savepath):
            os.makedirs(self.savepath)

    @property
    def history(self):
        return sorted([
            item for item in os.listdir(self.savepath)
            if self.startswith.search(item)
        ], reverse=True)

    def temporary(self):
        suffix = '.' + datetime.now().strftime(DATETIME_FORMAT)
        tmppath = os.path.join(self.savepath, self.basename + suffix)
        tmppath = self.archiver.compress(self.path, tmppath, isdir=self.isdir)
        history = self.history

        try:
            nochange = filecmp.cmp(
                os.path.join(self.savepath, history[0]),
                os.path.join(self.savepath, history[1])
            )
        except IndexError:
            nochange = False

        return nochange, tmppath

    def save(self, force=False):
        nochange, newpath = self.temporary()
        if not force and nochange:
            os.remove(newpath)

    def restore(self, force=False, refuge_current=True):
        history = self.history
        if not history:
            raise HistoryEmpty(os.listdir(self.savepath))

        nochange, curpath = self.temporary()
        latestpath = history[0]

        if force or not nochange:
            self.remove(self.path)
            archive = os.path.join(self.savepath, latestpath)
            self.archiver.decompress(archive, self.path, isdir=self.isdir)
            os.remove(archive)

        if refuge_current:
            sentence = curpath.rsplit('.', 2)
            sentence[1] = 'current'
            refugepath = '.'.join(sentence)
            shutil.move(curpath, refugepath)
        else:
            os.remove(curpath)
