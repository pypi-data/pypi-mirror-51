# Licensed under a 3-clause BSD style license - see LICENSE.rst
# -*- coding: utf-8 -*-
"""
hpsspy
~~~~~~

Python interface to the HPSS system.
"""


class HpssError(Exception):
    """Generic exception class for HPSS Errors.
    """
    pass


class HpssOSError(HpssError):
    """HPSS Errors that are similar to OSError.
    """
    pass


__version__ = '0.5.1'
