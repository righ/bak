# coding: utf-8
import re


class BaseArchiver(object):
    def __init__(self, **options):
        self.options = options
