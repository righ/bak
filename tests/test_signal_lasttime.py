# coding: utf-8
from datetime import datetime, timedelta
from unittest import TestCase
from .clean import CleanMixin


class TestLastTimeSignal(TestCase, CleanMixin):
    def setUp(self):
        self._copy('test.txt.sample', 'test.txt')
        self._copy('testdir.sample', 'testdir')

    def tearDown(self):
        self._clear()

    def _getTarget(self, *args, **kwargs):
        from bak.signal.lasttime import LastTimeSignal
        return LastTimeSignal(*args, **kwargs)

    def _getItem(self, *args, **kwargs):
        from bak.item import Item
        return Item(*args, **kwargs)

    def test_timedelta(self):
        path = self.pjoin('test.txt')
        savepath = self.pjoin('savedir/')

        item = self._getItem(path, savepath, timeunit='microsecond')
        item.save(force=True)

        bakname = item.history[0]
        savetime = datetime.strptime(bakname.split('.')[2], item._timeformat)
        future = savetime + timedelta(hours=1)

        ls = self._getTarget(timedelta(hours=1))
        self.assertTrue(ls.evalute(item, now=future))

        ls = self._getTarget(timedelta(hours=1, minutes=-1))
        self.assertFalse(ls.evalute(item, now=future))

        ls = self._getTarget(timedelta(minutes=59, seconds=59, microseconds=999999))
        self.assertFalse(ls.evalute(item, now=future))

    def test_dict(self):
        path = self.pjoin('test.txt')
        savepath = self.pjoin('savedir/')

        item = self._getItem(path, savepath, timeunit='microsecond')
        item.save(force=True)

        bakname = item.history[0]
        savetime = datetime.strptime(bakname.split('.')[2], item._timeformat)
        future = savetime + timedelta(hours=1)

        ls = self._getTarget({'hours': 1})
        self.assertTrue(ls.evalute(item, now=future))

        ls = self._getTarget({'hours': 1, 'minutes': -1})
        self.assertFalse(ls.evalute(item, now=future))

        ls = self._getTarget({'minutes': 59, 'seconds': 59, 'microseconds': 59})
        self.assertFalse(ls.evalute(item, now=future))

    def test_list(self):
        path = self.pjoin('test.txt')
        savepath = self.pjoin('savedir/')

        item = self._getItem(path, savepath, timeunit='microsecond')
        item.save(force=True)

        bakname = item.history[0]
        savetime = datetime.strptime(bakname.split('.')[2], item._timeformat)
        future = savetime + timedelta(hours=1)

        ls = self._getTarget([0, 0, 0, 0, 0, 1])
        self.assertTrue(ls.evalute(item, now=future))

        ls = self._getTarget([0, 0, 0, 0, -1, 1])
        self.assertFalse(ls.evalute(item, now=future))

        ls = self._getTarget([0, 59, 999, 999, 59])
        self.assertFalse(ls.evalute(item, now=future))

    def test_error(self):
        from bak.signal.lasttime import InvalidDeltaType
        with self.assertRaises(InvalidDeltaType):
            self._getTarget(None)
