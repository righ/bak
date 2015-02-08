Requirements
============
- Python 2.7

Install
=======

.. code-block:: sh

 $ pip install bak

Note
====
This library has not been tested enought yet.

Usage
=====

Basic Example
-------------

.. code-block:: python

 >>> import bak
 >>> item = bak.Item('test.txt')

 >>> # backup save
 >>> item.save()

 >>> # backup restore
 >>> item.restore()

History
=======
0.1.x
-----
- There is no change in the file(or directory), it does not save and restore.
- Added Exceptions.
- Added Tests.

0.0.x
-----
- First release.
