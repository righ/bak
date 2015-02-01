# coding: utf-8
import re


class BaseArchiver(object):
    def __init__(self, **options):
        self.options = options

    def set_exclude_rules(self, *exclude_rules):
        self.exclude_rules = [
            re.compile(rule)
            for rule in exclude_rules
        ]
        return self

