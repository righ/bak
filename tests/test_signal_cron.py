# coding: utf-8
from datetime import datetime as d
from unittest import TestCase


class TestCronSignal(TestCase):
    def _getTarget(self, *args, **kwargs):
        from bak.signal.cron import CronSignal
        return CronSignal(*args, **kwargs)

    def test_anytime(self):
        da = self._getTarget()
        self.assertTrue(da.evalute(None, now=d(1988, 5, 22, 10, 20, 30)))
        self.assertTrue(da.evalute(None, now=d(1, 1, 1, 0, 0, 0)))
        self.assertTrue(da.evalute(None, now=d(9999, 12, 31, 23, 59, 59)))

    def test_single_value(self):
        # 01-01 01:01 (sun)
        d1 = self._getTarget(1, 1, 1, 1, 0)
        # 01-01-01 01:01
        self.assertTrue(d1.evalute(None, now=d(1, 1, 1, 1, 1)))
        # 01-01-01 01:02
        self.assertFalse(d1.evalute(None, now=d(1, 1, 1, 1, 2)))
        # 01-01-01 02:01
        self.assertFalse(d1.evalute(None, now=d(1, 1, 1, 2, 1)))
        # 01-01-02 01:01
        self.assertFalse(d1.evalute(None, now=d(1, 1, 2, 1, 1)))
        # 01-02-01 01:01
        self.assertFalse(d1.evalute(None, now=d(1, 2, 1, 1, 1)))

    def test_multiple_value(self):
        # 01-01 01:01 (*)
        d1 = self._getTarget('0,30', '0,12', '1,15', '1,6', '*')
        # 01-01-01 00:00
        self.assertTrue(d1.evalute(None, now=d(1, 1, 1, 0, 0)))
        # 01-01-01 00:30
        self.assertTrue(d1.evalute(None, now=d(1, 1, 1, 0, 30)))
        # 01-01-01 00:31
        self.assertFalse(d1.evalute(None, now=d(1, 1, 1, 0, 31)))
        # 01-01-01 12:00
        self.assertTrue(d1.evalute(None, now=d(1, 1, 1, 12, 0)))
        # 01-01-01 13:00
        self.assertFalse(d1.evalute(None, now=d(1, 1, 1, 13, 0)))
        # 01-01-15 00:00
        self.assertTrue(d1.evalute(None, now=d(1, 1, 15, 0, 0)))
        # 01-01-16 00:00
        self.assertFalse(d1.evalute(None, now=d(1, 1, 16, 0, 0)))
        # 01-06-01 00:00
        self.assertTrue(d1.evalute(None, now=d(1, 6, 1, 0, 0)))
        # 01-07-01 00:00
        self.assertFalse(d1.evalute(None, now=d(1, 7, 1, 0, 0)))

    def test_range_value(self):
        # (10-12)-(10-15) (12-23):(0-30) (*)
        dr = self._getTarget('1-30', '12-22', '10-15', '10-11', '*')
        # 2000-10-10 12:01
        self.assertTrue(dr.evalute(None, now=d(2000, 10, 10, 12, 1)))
        # 2000-12-15 22:30
        self.assertTrue(dr.evalute(None, now=d(2000, 11, 15, 22, 30)))
        # 2000-09-10 12:01
        self.assertFalse(dr.evalute(None, now=d(2000, 9, 10, 12, 1)))
        # 2000-13-10 12:01
        self.assertFalse(dr.evalute(None, now=d(2000, 12, 10, 12, 1)))
        # 2000-10-09 12:01
        self.assertFalse(dr.evalute(None, now=d(2000, 10, 9, 12, 1)))
        # 2000-10-16 12:01
        self.assertFalse(dr.evalute(None, now=d(2000, 10, 16, 12, 1)))
        # 2000-10-10 11:01
        self.assertFalse(dr.evalute(None, now=d(2000, 10, 10, 11, 1)))
        # 2000-10-10 23:01
        self.assertFalse(dr.evalute(None, now=d(2000, 10, 10, 23, 1)))
        # 2000-10-10 12:00
        self.assertFalse(dr.evalute(None, now=d(2000, 10, 10, 12, 0)))
        # 2000-10-10 12:31
        self.assertFalse(dr.evalute(None, now=d(2000, 10, 10, 12, 31)))

        dr = self._getTarget('0-59', '0-23', '1-31', '1-12', 'mon-wed')
        # sun
        self.assertFalse(dr.evalute(None, now=d(1, 1, 1)))
        # mon
        self.assertTrue(dr.evalute(None, now=d(1, 1, 2)))
        # tue
        self.assertTrue(dr.evalute(None, now=d(1, 1, 3)))
        # wed
        self.assertTrue(dr.evalute(None, now=d(1, 1, 4)))
        # thu
        self.assertFalse(dr.evalute(None, now=d(1, 1, 5)))

    def test_interval_value(self):
        # (*/2)-(*/5) (*/3):(*/10) (*)
        di = self._getTarget('*/10', '*/3', '*/5', '*/2', '*')
        # 2000-03-06 03:10
        self.assertTrue(di.evalute(None, now=d(2000, 3, 6, 3, 10)))
        # 2000-03-06 03:40
        self.assertTrue(di.evalute(None, now=d(2000, 3, 6, 3, 40)))
        # 2000-03-06 09:10
        self.assertTrue(di.evalute(None, now=d(2000, 3, 6, 9, 10)))
        # 2000-03-16 03:10
        self.assertTrue(di.evalute(None, now=d(2000, 3, 16, 3, 10)))

        # 2000-03-06 03:09
        self.assertFalse(di.evalute(None, now=d(2000, 3, 6, 3, 9)))
        # 2000-03-06 02:40
        self.assertFalse(di.evalute(None, now=d(2000, 3, 6, 2, 40)))
        # 2000-03-05 09:10
        self.assertFalse(di.evalute(None, now=d(2000, 3, 5, 9, 10)))
        # 2000-02-16 03:10
        self.assertFalse(di.evalute(None, now=d(2000, 2, 16, 3, 10)))

        # (*)-(*) (*):(*) (*/2)
        di = self._getTarget('*', '*', '*', '*', '*/2')
        # sun
        self.assertTrue(di.evalute(None, now=d(1, 1, 1)))
        # mon
        self.assertFalse(di.evalute(None, now=d(1, 1, 2)))
        # tue
        self.assertTrue(di.evalute(None, now=d(1, 1, 3)))
        # wed
        self.assertFalse(di.evalute(None, now=d(1, 1, 4)))
        # thu
        self.assertTrue(di.evalute(None, now=d(1, 1, 5)))
        # fri
        self.assertFalse(di.evalute(None, now=d(1, 1, 6)))
        # sat
        self.assertTrue(di.evalute(None, now=d(1, 1, 7)))
        # sun
        self.assertTrue(di.evalute(None, now=d(1, 1, 8)))

    def test_complex_combination(self):
        # (1,10-12)-(*/3,12) (*/2,*/3):(10-20/2) (*)
        dc = self._getTarget('10-20/2', '*/2,*/3', '*/3,12', '1,10-12', '*')
        # 01-01-01 00:10
        self.assertTrue(dc.evalute(None, now=d(1, 1, 1, 0, 10)))
        # 01-01-01 00:14
        self.assertTrue(dc.evalute(None, now=d(1, 1, 1, 0, 14)))
        # 01-01-01 00:15
        self.assertFalse(dc.evalute(None, now=d(1, 1, 1, 0, 15)))
        # 01-01-01 00:20
        self.assertTrue(dc.evalute(None, now=d(1, 1, 1, 0, 20)))

        # 01-01-01 02:10
        self.assertTrue(dc.evalute(None, now=d(1, 1, 1, 2, 10)))
        # 01-01-01 03:10
        self.assertTrue(dc.evalute(None, now=d(1, 1, 1, 3, 10)))
        # 01-01-01 04:10
        self.assertTrue(dc.evalute(None, now=d(1, 1, 1, 4, 10)))
        # 01-01-01 05:10
        self.assertFalse(dc.evalute(None, now=d(1, 1, 1, 5, 10)))
        # 01-01-01 06:10
        self.assertTrue(dc.evalute(None, now=d(1, 1, 1, 6, 10)))

        # 01-01-09 00:10
        self.assertFalse(dc.evalute(None, now=d(1, 1, 9, 0, 10)))
        # 01-01-10 00:10
        self.assertTrue(dc.evalute(None, now=d(1, 1, 10, 0, 10)))
        # 01-01-11 00:10
        self.assertFalse(dc.evalute(None, now=d(1, 1, 11, 0, 10)))
        # 01-01-12 00:10
        self.assertTrue(dc.evalute(None, now=d(1, 1, 12, 0, 10)))

        # 01-09-01 00:10
        self.assertFalse(dc.evalute(None, now=d(1, 9, 1, 0, 10)))
        # 01-10-01 00:10
        self.assertTrue(dc.evalute(None, now=d(1, 10, 1, 0, 10)))
        # 01-11-01 00:10
        self.assertTrue(dc.evalute(None, now=d(1, 11, 1, 0, 10)))
        # 01-12-01 00:10
        self.assertTrue(dc.evalute(None, now=d(1, 12, 1, 0, 10)))
