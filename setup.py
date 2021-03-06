#!/usr/bin/env python
# coding: utf-8

from setuptools import setup, find_packages
from bak import (
    __version__,
    __license__,
    __author__,
    __author_email__,
)

__name__ = 'bak'
__url__ = 'https://bitbucket.org/crohaco/bak'

__short_description__ = 'simple file backup library.'
__long_description__ = open('./README.rst', 'r').read()

__classifiers__ = [
    'Environment :: Console',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: Apache Software License',
    'Programming Language :: Python',
    'Topic :: Software Development',
]
__keywords__ = [
    'backup',
]


setup(
    name=__name__,
    version=__version__,
    description=__short_description__,
    long_description=__long_description__,
    classifiers=__classifiers__,
    keywords=' ,'.join(__keywords__),
    author=__author__,
    author_email=__author_email__,
    url=__url__,
    license=__license__,
    packages=find_packages(exclude=['*.tests', '*.tests.*']),
)
