# coding: utf-8

from unittest import TestCase
from .clean import CleanMixin


class ItemTest(TestCase, CleanMixin):
    def setUp(self):
        self._copy('test.txt.sample', 'test.txt')
        self._copy('testdir.sample', 'testdir')

    def tearDown(self):
        self._clear()

    def _callFUT(self, *args, **kwargs):
        from bak.item import Item
        return Item(*args, **kwargs)

    def test_target_not_exist(self):
        from bak.exception import ItemNotFound
        with self.assertRaises(ItemNotFound):
            self._callFUT('nofiletest.txt', savepath=self.pjoin('savedir'))

    def test_invalid_basename(self):
        from bak.exception import ItemPathInvalid
        with self.assertRaises(ItemPathInvalid):
            self._callFUT('/')

    def test_save(self):
        path = self.pjoin('testdir/')
        savepath = self.pjoin('savedir/')
        item = self._callFUT(path, savepath, timeunit='microsecond')
        self.assertEqual(len(item.archives), 0)
        item.save()
        self.assertEqual(len(item.archives), 1)
        item.save(force=True)
        self.assertEqual(len(item.archives), 2)
        item.save()
        self.assertEqual(len(item.archives), 2)
        with open(path+'/a.txt', 'wb') as f:
            f.write(u'changed'.encode('utf-8'))
        item.save()
        self.assertEqual(len(item.archives), 3)

    def test_restore(self):
        from bak.exception import ArchivesEmpty

        path = self.pjoin('test.txt')
        item = self._callFUT(path, savepath=self.pjoin('savedir'), timeunit='microsecond')
        with self.assertRaises(ArchivesEmpty):
            item.restore()
        item.save()
        item.restore()
        self.assertEqual(len(item.archives), 1)
        item.restore(force=True)
        self.assertEqual(len(item.archives), 0)
