# coding: utf-8
from datetime import datetime
from .base import BaseSignal


class ScheduleSignal(BaseSignal):
    def __init__(self, minute='*', hour='*', day='*', month='*', week='*'):
        self.timerule = {
            'minute': str(minute),
            'hour': str(hour),
            'day': str(day),
            'month': str(month),
            'week': {
                'sun': '0',
                'mon': '1',
                'tue': '2',
                'wed': '3',
                'thu': '4',
                'fri': '5',
                'sat': '6',
            }.get(str(week).lower(), str(week)),
        }

    def evalute(self, item, **env):
        now = env.get('now', datetime.now())
        for unit, times in self.timerule.items():
            times = times.replace('*', {
                'minute': '0-60',
                'hour': '0-23',
                'day': '1-31',
                'month': '1-12',
                'week': '0-7',
            }[unit])
            for time in times.split(','):
                if '/' in time:
                    time, interval = time.split('/')
                else:
                    interval = 1

                if '-' in time:
                    starttime, endtime = time.split('-')
                else:
                    starttime, endtime = time, time

                rangeargs = map(int, (starttime, endtime, interval))
                rangeargs[1] += 1

                unitnow = getattr(now, unit)
                unitnow = unitnow() if callable(unitnow) else unitnow
                if unitnow not in range(*rangeargs):
                    return False

        return True
