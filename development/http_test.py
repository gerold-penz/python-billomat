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

# invoice_items_iterator = pybillomat.InvoiceItemsIterator(conn = conn)
# invoice_items_iterator.search(invoice_id = 1078526)
# for invoice_item in invoice_items_iterator:
#     print invoice_item

