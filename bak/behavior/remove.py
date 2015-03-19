# coding: utf-8

from .base import BaseBehavior


class RemoveBehavior(BaseBehavior):
    def __init__(self, *indexes):
        """
        """
        assert 1 <= len(indexes) <= 3

        self.indexes = indexes

    def execute(self, item, **env):
        item.remove(*self.indexes)
