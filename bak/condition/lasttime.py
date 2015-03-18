# coding: utf-8
from datetime import datetime
try:
    from dateutil.relativedelta import relativedelta as timedelta
except ImportError:
    from datetime import timedelta

from .base import BaseCondition
from ..exception import BakException


class InvalidDeltaType(BakException):
    pass


class LastTimeCondition(BaseCondition):
    def __init__(self, delta):
        if isinstance(delta, dict):
            self.delta = timedelta(**delta)
        elif isinstance(delta, (list, tuple)):
            self.delta = timedelta(*delta)
        elif isinstance(delta, timedelta):
            self.delta = delta
        else:
            raise InvalidDeltaType(delta)

    def evalute(self, item, **env):
        try:
            lasttime = datetime.strptime(item.history[0], item.datetime_format)
        except IndexError:
            return False

        now = env.get('now', datetime.now())
        return lasttime + self.delta > now
