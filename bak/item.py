# coding: utf-8

import os
import re
import shutil
import filecmp

from datetime import datetime
from .archive.tar import TBZArchiver
from .handler import Handler
from .exception import (
    ItemNotFound,
    ItemPathInvalid,
    ArchivesEmpty,
    InvalidDatetimeUnit,
)

BASE_TIMEFORMAT = '%Y%m%d%H%M%S%f'


class Item(object):
    def __repr__(self):
        return '<{0} ({1})>'.format(self._basename, len(self.archives))

    def __init__(
        self,
        path,
        savepath=None,
        archiver=TBZArchiver,
        timeunit='second',
        **options
    ):
        self._path = path.rstrip('/')
        self._basename = os.path.basename(self._path)

        try:
            index = {
                'year': 2, 'month': 4, 'day': 6,
                'hour': 8, 'minute': 10, 'second': 12, 'microsecond': 14,
            }[timeunit.lower()]
            self._timeformat = BASE_TIMEFORMAT[:index]
        except KeyError:
            raise InvalidDatetimeUnit

        self._startswith = re.compile('^{basename}\.{suffix}'.format(
            basename=re.escape(self._basename),
            suffix=r'(\d{4,21})'
        ))

        abspath = os.path.realpath(path)
        if not os.path.exists(abspath):
            raise ItemNotFound(abspath)

        self.options = options
        self._archiver = archiver(**options)

        self._isdir = os.path.isdir(abspath)
        if self._isdir:
            self._remove = shutil.rmtree
        else:
            self._remove = os.remove

        for self._basename in reversed(abspath.split('/')):
            if self._basename:
                break
        else:
            raise ItemPathInvalid(abspath)

        # if no problem, make save dir
        self._savepath = savepath or os.path.dirname(self._path) or './'
        if not os.path.exists(self._savepath):
            os.makedirs(self._savepath)

        self.handlers = []

    @property
    def archives(self):
        return sorted([
            item for item in os.listdir(self._savepath)
            if self._startswith.search(item)
        ], reverse=True)

    def _temporary(self):
        suffix = '.' + datetime.now().strftime(self._timeformat)
        tmppath = os.path.join(self._savepath, self._basename + suffix)
        tmppath = self._archiver.compress(self._path, tmppath, isdir=self._isdir)
        archives = self.archives

        try:
            nochange = filecmp.cmp(
                os.path.join(self._savepath, archives[0]),
                os.path.join(self._savepath, archives[1])
            )
        except IndexError:
            nochange = False

        return nochange, tmppath

    def save(self, force=False):
        nochange, newpath = self._temporary()
        if not force and nochange:
            os.remove(newpath)
        self.trigger(**self.options)

    def restore(self, force=False, refuge_current=True):
        archives = self.archives
        if not archives:
            raise ArchivesEmpty(os.listdir(self._savepath))

        nochange, curpath = self._temporary()
        latestpath = archives[0]

        if force or not nochange:
            self._remove(self._path)
            archive = os.path.join(self._savepath, latestpath)
            self._archiver.decompress(archive, self._path, isdir=self._isdir)
            os.remove(archive)

        if refuge_current:
            sentence = curpath.rsplit('.', 2)
            sentence[1] = 'current'
            refugepath = '.'.join(sentence)
            shutil.move(curpath, refugepath)
        else:
            os.remove(curpath)

    def remove(self, *indexes):
        assert 1 <= len(indexes) <= 3

        if len(indexes) == 1:
            i = indexes[0]
            if i >= 0:
                indexes = slice(i, i+1)
            elif i == -1:
                indexes = slice(-1, None)
            else:
                indexes = slice(i-1, i)
        else:
            indexes = slice(*indexes)

        for archivename in self.archives[indexes]:
            archivepath = os.path.join(self._savepath, archivename)
            os.remove(archivepath)

    def on(self, behavior, signal):
        handler = Handler(behavior, signal)
        self.handlers.append(handler)
        return self

    def trigger(self, **env):
        for handler in self.handlers:
            handler.trigger(self, **env)
