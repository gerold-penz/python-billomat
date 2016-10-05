#!/usr/bin/env python
# coding: utf-8
"""
Errors
"""


class BillomatError(RuntimeError):
    pass


class EmptyFilterError(BillomatError):
    pass


class NoIdError(BillomatError):
    pass


class NotFoundError(BillomatError):
    pass


