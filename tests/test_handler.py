# coding: utf-8
from unittest import TestCase
from .clean import CleanMixin


class TestHandler(TestCase, CleanMixin):
    def setUp(self):
        self._copy('test.txt.sample', 'test.txt')
        self._copy('testdir.sample', 'testdir')

    def tearDown(self):
        self._clear()

    def _callFUT(self, *args, **kwargs):
        from bak.item import Item
        return Item(*args, **kwargs)

    def test_rotation(self):
        from bak.signal.fill import FillSignal
        from bak.behavior.remove import RemoveBehavior

        item = self._callFUT(
            self.pjoin('test.txt'),
            savepath=self.pjoin('savedir'),
            timeunit='microsecond')
        item.on(FillSignal(3), RemoveBehavior(-1))
        for i in range(10):
            item.save(force=True)
            self.assertTrue(len(item.archives) <= 3)
