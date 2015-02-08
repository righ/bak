# coding: utf-8

class BakException(Exception):
    pass


class ItemNotFound(BakException):
    pass


class ItemPathInvalid(BakException):
    pass


class HistoryEmpty(BakException):
    pass
