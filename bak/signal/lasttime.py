# coding: utf-8
from datetime import datetime, timedelta
typedelta = (timedelta,)

try:
    from dateutil.relativedelta import relativedelta
    typedelta += (relativedelta,)
except ImportError:
    pass

from .base import BaseSignal
from ..exception import BakException


class InvalidDeltaType(BakException):
    pass


class LastTimeSignal(BaseSignal):
    def __init__(self, delta, missing=True):
        if isinstance(delta, dict):
            self.delta = timedelta(**delta)
        elif isinstance(delta, (list, tuple)):
            self.delta = timedelta(*delta)
        elif isinstance(delta, typedelta):
            self.delta = delta
        else:
            raise InvalidDeltaType(delta)
        self.missing = missing

    def evalute(self, item, **env):
        try:
            baktime = item.history[0][len(item._basename)+1:]
            lasttime = datetime.strptime(baktime.split('.')[0], item._timeformat)
        except IndexError:
            return self.missing

        now = env.get('now', datetime.now())
        return lasttime + self.delta >= now
