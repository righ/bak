# coding: utf-8
import os
import shutil

prefix = 'tests/files'


class CleanMixin(object):
    def pjoin(self, path):
        return os.path.join(prefix, path)

    def _clear(self):
        for filename in os.listdir(prefix):
            if filename not in ('test.txt.sample', 'testdir.sample'):
                self._remove(filename)

    def _remove(self, path):
        path = self.pjoin(path)
        try:
            if os.path.isdir(path):
                remove = shutil.rmtree
            else:
                remove = os.remove
            remove(path)
        except OSError:
            pass

    def _copy(self, src, dst):
        self._remove(dst)
        src = self.pjoin(src)
        dst = self.pjoin(dst)
        if os.path.isdir(src):
            copy = shutil.copytree
        else:
            copy = shutil.copy

        copy(src, dst)
