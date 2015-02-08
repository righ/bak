# coding: utf-8
import os
import shutil
from unittest import TestCase

prefix = 'tests/files'
def pjoin(path):
    return os.path.join(prefix, path)


class ItemTest(TestCase):
    def _clear(self):
        for filename in os.listdir(prefix):
            if filename not in ('test.txt.sample', 'testdir.sample'):
                self._remove(filename)

    def _remove(self, path):
        path = pjoin(path)
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
        src = pjoin(src)
        dst = pjoin(dst)
        if os.path.isdir(src):
            copy = shutil.copytree
        else:
            copy = shutil.copy

        copy(src, dst)

    def _callFUT(self, *args, **kwargs):
        from bak.item import Item
        return Item(*args, **kwargs)

    def setUp(self):
        self._copy('test.txt.sample', 'test.txt')
        self._copy('testdir.sample', 'testdir')

    def tearDown(self):
        self._clear()

    def test_target_not_exist(self):
        from bak.exception import (
            ItemNotFound,
        )
        with self.assertRaises(ItemNotFound):
            self._callFUT('nofiletest.txt')

    def test_invalid_basename(self):
        from bak.exception import (
            ItemPathInvalid,
        )
        with self.assertRaises(ItemPathInvalid):
            self._callFUT('/')

    def test_save(self):
        path = pjoin('testdir/')
        savepath = pjoin('savedir/')
        item = self._callFUT(path, savepath)
        self.assertEqual(len(item.history), 0)
        item.save()
        self.assertEqual(len(item.history), 1)
        item.save(force=True)
        self.assertEqual(len(item.history), 2)
        item.save()
        self.assertEqual(len(item.history), 2)
        with open(path+'/a.txt', 'wb') as f:
            f.write('changed')
        item.save()
        self.assertEqual(len(item.history), 3)

    def test_restore(self):
        from bak.exception import (
            HistoryEmpty,
        )

        path = pjoin('test.txt')
        item = self._callFUT(path)
        with self.assertRaises(Exception):
            item.restore()
        item.save()
        item.restore()
        self.assertEqual(len(item.history), 1)
        item.restore(force=True)
        self.assertEqual(len(item.history), 0)
