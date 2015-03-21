# coding: utf-8
from .base import BaseSignal


class FillSignal(BaseSignal):
    def __init__(self, number):
        self.number = number

    def evalute(self, item, **env):
        return len(item.history) >= self.number
