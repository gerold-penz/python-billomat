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


class InvoiceNotFoundError(BillomatError):
    pass


class ClientNotFoundError(BillomatError):
    pass


class NoClientLoaded(BillomatError):
    pass


class NoInvoiceLoaded(BillomatError):
    pass

