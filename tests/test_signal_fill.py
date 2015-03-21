# coding: utf-8
from unittest import TestCase
from .clean import CleanMixin


class TestFillSignal(TestCase, CleanMixin):
    def setUp(self):
        self._copy('test.txt.sample', 'test.txt')
        self._copy('testdir.sample', 'testdir')

    def tearDown(self):
        self._clear()

    def _getTarget(self, *args, **kwargs):
        from bak.signal.fill import FillSignal
        return FillSignal(*args, **kwargs)

    def _getItem(self, *args, **kwargs):
        from bak.item import Item
        return Item(*args, **kwargs)

    def test_it(self):
        path = self.pjoin('test.txt')
        savepath = self.pjoin('savedir/')

        item = self._getItem(path, savepath, timeunit='microsecond')
        for i in range(5):
            item.save(force=True)

        f4 = self._getTarget(4)
        self.assertFalse(f4.evalute(item))

        f5 = self._getTarget(5)
        self.assertTrue(f5.evalute(item))

        f6 = self._getTarget(6)
        self.assertTrue(f6.evalute(item))
