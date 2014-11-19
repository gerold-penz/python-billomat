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


class InvoiceNotFoundError(NotFoundError):
    pass


class ClientNotFoundError(NotFoundError):
    pass


class NoClientLoaded(BillomatError):
    pass


class NoInvoiceLoaded(BillomatError):
    pass

