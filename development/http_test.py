#!/usr/bin/env python
# coding: utf-8

# BEGIN --- required only for testing, remove in real world code --- BEGIN
import os
import sys
THISDIR = os.path.dirname(os.path.abspath(__file__))
APPDIR = os.path.abspath(os.path.join(THISDIR, os.path.pardir))
sys.path.insert(0, APPDIR)
import _personal_billomat_data as _personal
# END --- required only for testing, remove in real world code --- END


import pybillomat


conn = pybillomat.Connection(
    billomat_id = _personal.gerolds_billomat_id,
    billomat_api_key = _personal.gerolds_billomat_api_key,
    billomat_app_id = _personal.gerolds_billomat_app_id,
    billomat_app_secret = _personal.gerolds_billomat_app_secret
)

# invoice_payments_iterator = pybillomat.InvoicePaymentsIterator(
#     conn = conn, per_page = 10
# )
# invoice_payments_iterator.search(order_by = u"date")
#
# for invoice_payment in invoice_payments_iterator[:10]:
#     assert isinstance(invoice_payment, pybillomat.InvoicePayment)
#
#     print repr(invoice_payment)
#     print


invoice_payment = pybillomat.InvoicePayment.create(
    conn = conn,
    invoice_id = 1271007,
    amount = 23.52,
    comment = u"Zahlung dankend erhalten.",
    mark_invoice_as_paid = True
)
