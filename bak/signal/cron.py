# coding: utf-8
from datetime import datetime
from .base import BaseSignal
from ..exception import BakException


class InvalidTimeFormat(BakException):
    message = '[]'


def week_replace(s):
    s = str(s).lower()
    for before, after in {
        'sun': '0',
        'mon': '1',
        'tue': '2',
        'wed': '3',
        'thu': '4',
        'fri': '5',
        'sat': '6',
    }.items():
        s = s.replace(before, after)
    return s


class CronSignal(BaseSignal):
    def __init__(self, minute='*', hour='*', day='*', month='*', week='*'):
        self.timerule = {
            'minute': str(minute),
            'hour': str(hour),
            'day': str(day),
            'month': str(month),
            'weekday': week_replace(week),
        }

    def evalute(self, item, **env):
        now = env.get('now', datetime.now())
        for unit, times in self.timerule.items():
            times = times.replace('*', {
                'minute': '0-59',
                'hour': '0-23',
                'day': '1-31',
                'month': '1-12',
                'weekday': '0-7',
            }[unit])
            for time in times.split(','):
                if not time:
                    continue

                if '/' in time:
                    time, interval = time.split('/')
                else:
                    interval = 1

                interval = int(interval)

                if '-' in time:
                    starttime, endtime = time.split('-')
                else:
                    starttime, endtime = time, time

                starttime, endtime = int(starttime), int(endtime)+1

                unitnow = getattr(now, unit)
                unitnow = unitnow() if callable(unitnow) else unitnow
                if unitnow in range(starttime, endtime, interval):
                    break
            else:
                return False

        return True
