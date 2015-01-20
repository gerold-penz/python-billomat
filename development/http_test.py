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
import datetime


conn = pybillomat.Connection(
    billomat_id = _personal.gerolds_billomat_id,
    billomat_api_key = _personal.gerolds_billomat_api_key,
    billomat_app_id = _personal.gerolds_billomat_app_id,
    billomat_app_secret = _personal.gerolds_billomat_app_secret
)



# invoices_iterator = pybillomat.InvoicesIterator(conn = conn)
# invoices_iterator.search(status = "DRAFT")
# for invoice in invoices_iterator:
#     print invoice
#
#     # invoice.edit(date = datetime.date(2015, 1, 9))
#
#
#



email_template = pybillomat.EmailTemplate(conn = conn, id = 248227)
print email_template
# email_template.edit(
#     name = u"TEST TEST",
#     type = u"INVOICES"
# )
