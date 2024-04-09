snakehouse
==========
![Build status](https://github.com/smok-serwis/snakehouse/actions/workflows/ci.yml/badge.svg)
[![Code Climate](https://codeclimate.com/github/smok-serwis/snakehouse/badges/gpa.svg)](https://codeclimate.com/github/smok-serwis/snakehouse)
[![Issue Count](https://codeclimate.com/github/smok-serwis/snakehouse/badges/issue_count.svg)](https://codeclimate.com/github/smok-serwis/snakehouse)
[![PyPI](https://img.shields.io/pypi/pyversions/snakehouse.svg)](https://pypi.python.org/pypi/snakehouse)
[![PyPI version](https://badge.fury.io/py/snakehouse.svg)](https://badge.fury.io/py/snakehouse)
[![PyPI](https://img.shields.io/pypi/implementation/snakehouse.svg)](https://pypi.python.org/pypi/snakehouse)
[![PyPI](https://img.shields.io/pypi/wheel/snakehouse.svg)]()
[![Documentation Status](https://readthedocs.org/projects/snakehouse/badge/?version=latest)](http://snakehouse.readthedocs.io/en/latest/?badge=latest)
[![License](https://img.shields.io/pypi/l/snakehouse)](https://github.com/smok-serwis/snakehouse)

snakehouse is a tool to pack mutiple .pyx files
into a single extension.

Inspired by [this StackOverflow discussion](https://stackoverflow.com/questions/30157363/collapse-multiple-submodules-to-one-cython-extension).

Tested and works on CPython 3.5-3.12, 
both Windows and [Linux](https://travis-ci.org/github/smok-serwis/snakehouse).

It doesn't work on PyPy due to lack of
`PyModule_FromDefAndSpec` symbol.

READ BEFORE YOU USE
===================

Be sure to read the [docs](http://snakehouse.readthedocs.io/en/latest/) 
before you start using it.
