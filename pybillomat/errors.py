#!/usr/bin/env python
# coding: utf-8
"""
Errors
"""


class BillomatError(RuntimeError):
    pass


class EmptyFilterError(BillomatError):
    pass

