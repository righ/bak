Requirements
============
- Python 2.7
- Python 3.4

Install
=======

.. code-block:: sh

 $ pip install bak

Usage
=====

Basic Example
-------------

**save**

.. code-block:: python

 In [1]: !cat test.txt
 test

 In [2]: import bak
 In [3]: item = bak.Item('test.txt', 'savedir')
 # item save as archive in the savedir.(default tar bz2)
 # it is same folder with item if savepath is not specified.
 In [4]: item.save()
 In [5]: !ls savedir/
 test.txt.20150321200204.tbz

 # item does not save if it has no change.
 In [6]: item.save()
 In [7]: !ls savedir/
 test.txt.20150321200204.tbz

 # if you want save item that has no change, specify force option.
 In [8]: item.save(force=True)
 In [9]: !ls savedir/
 test.txt.20150321200204.tbz  test.txt.20150321200227.tbz

 # confirm backup files as item.archives.
 In [10]: item.archives
 Out[10]: ['test.txt.20150321200227.tbz', 'test.txt.20150321200204.tbz']


**restore**

.. code-block:: python

 In [11]: !echo 'change!' > test.txt
 In [12]: item.restore()
 In [13]: !cat test.txt
 test

 # Normally, item saves it as current-archive the current item in the same folder.
 In [14]: !ls savedir/
 test.txt.20150321200204.tbz  test.txt.current.tbz

 # item.archives does not contain current-archive.
 In [15]: item.archives
 Out[15]: ['test.txt.20150321200204.tbz']

 # item does not restore if it has no change.
 In [16]: item.restore()
 In [17]: !ls savedir/
 test.txt.20150321200204.tbz  test.txt.current.tbz

 In [18]: !rm savedir/test.txt.current.tbz
 # if specified refuge_current "false", current-archive does not save.
 In [19]: item.restore(force=True, refuge_current=False)
 In [20]: !ls savedir/


Rotation Example
----------------
This is a sample to delete from the oldest archive.

.. code-block:: python

 In [1]: import bak
 In [2]: item = bak.Item('test.txt', 'savedir')

 # add handler by item.on, specify Signal and Behavior set.
 # FillSignal: archive number reaches value specified, execute behavior.
 # RemoveBehavior: remove specified index(es) of archive(s).
 In [3]: item.on(bak.FillSignal(3), bak.RemoveBehavior(-1))
 Out[3]: <test.txt (0)>

 In [4]: item.archives
 Out[4]: []

 In [5]: item.save(force=True)
 In [6]: item.archives
 Out[6]: ['test.txt.20150321204308.tbz']

 In [7]: item.save(force=True)
 In [8]: item.archives
 Out[8]: ['test.txt.20150321204313.tbz', 'test.txt.20150321204308.tbz']

 In [9]: item.save(force=True)
 In [10]: item.archives
 Out[10]: ['test.txt.20150321204319.tbz', 'test.txt.20150321204313.tbz']


History
=======
0.2.x
-----
- Added handler function with the following.

    - Signal(FillSignal, CronSignal, LastTimeSignal)
    - Behavior(RemoveBehavior only)

- history attribute renamed to archives.

0.1.x
-----
- There is no change in the file(or directory), it does not save and restore.
- Added Exceptions.
- Added Tests.

0.0.x
-----
- First release.


TODO
----
- make the reference.
- add FTP Behavior.
- provide command.
