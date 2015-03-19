# coding: utf-8
from .base import BaseSignal


class NumberCondition(BaseSignal):
    def __init__(self, number):
        self.number = number

    def evalute(self, item, **env):
        return self.number >= len(item.history)
