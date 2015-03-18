# coding: utf-8
import os
from .base import BaseBehavior


class RemoveBehavior(BaseBehavior):
    def __init__(self, *args):
        """
        """
        assert 1 <= len(args) <= 3

        if len(args) == 1:
            i = args[0]
            if i >= 0:
                self.slice = slice(i, i+1)
            else:
                self.slice = slice(i-1, i)
        else:
            self.slice = slice(*args)

    def execute(self, item, **env):
        for archivename in item.history[self.slice]:
            archivepath = os.path.join(item.savepath, archivename)
            os.remove(archivepath)
