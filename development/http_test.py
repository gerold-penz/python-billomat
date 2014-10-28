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
import pybillomat.http

conn = pybillomat.Connection(
    billomat_id = _personal.gerolds_billomat_id,
    billomat_api_key = _personal.gerolds_billomat_api_key,
    billomat_app_id = _personal.gerolds_billomat_app_id,
    billomat_app_secret = _personal.gerolds_billomat_app_secret
)

client = pybillomat.Client(conn = conn)
client.load_data(id = 422909)
print client

# invoices = pybillomat.Invoices(conn)
# invoices.search(client_id = 422909, status = "OPEN")
# print len(invoices)
#
# invoices[0].complete()

# invoice = pybillomat.Invoice(conn = conn, id = 981936)
# invoice.load()
# print invoice

# invoice = pybillomat.Invoice(conn, id = 982256)
# invoice.complete()
