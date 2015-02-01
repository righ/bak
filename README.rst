Requirements
============
- Python 2.7

Install
=======

.. code-block:: sh

 $ pip install bak


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

0.0.x
-----
- First release.
