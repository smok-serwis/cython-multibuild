snakehouse
==========
[![Build Status](https://travis-ci.org/smok-serwis/snakehouse.svg)](https://travis-ci.org/smok-serwis/snakehouse)
[![Code Climate](https://codeclimate.com/github/smok-serwis/snakehouse/badges/gpa.svg)](https://codeclimate.com/github/smok-serwis/snakehouse)
[![Issue Count](https://codeclimate.com/github/smok-serwis/snakehouse/badges/issue_count.svg)](https://codeclimate.com/github/smok-serwis/snakehouse)
[![PyPI](https://img.shields.io/pypi/pyversions/snakehouse.svg)](https://pypi.python.org/pypi/snakehouse)
[![PyPI version](https://badge.fury.io/py/snakehouse.svg)](https://badge.fury.io/py/snakehouse)
[![PyPI](https://img.shields.io/pypi/implementation/snakehouse.svg)](https://pypi.python.org/pypi/snakehouse)
[![PyPI](https://img.shields.io/pypi/wheel/snakehouse.svg)]()
[![license](https://img.shields.io/github/license/mashape/apistatus.svg)]()

snakehouse is a tool to pack mutiple .pyx files
into a single extension.

_There's a **MANDATORY READING** part at the end of this README. Read it or you will be sure to run into trouble._

Inspired by [this StackOverflow discussion](https://stackoverflow.com/questions/30157363/collapse-multiple-submodules-to-one-cython-extension).

Tested and works on CPython 3.5-3.9, 
both Windows and [Linux](https://travis-ci.org/github/smok-serwis/snakehouse).
It doesn't work on PyPy.

Contributions most welcome! If you contribute, feel free to attach
a change to [CONTRIBUTORS.md](/CONTRIBUTORS.md) as 
a part of your pull request as well!
Note what have you changed in
[CHANGELOG.md](/CHANGELOG.md) as well!

Usage notes - MANDATORY READING
-------------------------------
Take a look at [example](example/) on how to multi-build your Cython extensions.

Don't place modules compiled that way in root .py file's top level imports.
Wrap them in a layer of indirection instead!

This applies to unit tests as well!

When something goes wrong (eg. the application throws an unhandled exception)
the built module has a tendency to dump core.
Try to debug it first by passing `dont_snakehouse=True` to your
modules in the debug mode.

Also note that if you are compiling in `dont_snakehouse`
mode then your modules should have at least one of the following:
* a normal Python `def`
* a normal Python class (not `cdef class`)
* a line of Python initialization, eg.

```python
a = None
```

or 
```python
import logging

logger = logging.getLogger(__name__)
```

Otherwise `PyInit` won't be generated by Cython 
and such module will be unimportable in Python. Normal import won't suffice.
