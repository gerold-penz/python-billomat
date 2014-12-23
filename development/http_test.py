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

recurring = pybillomat.Recurring(conn)
recurring.load(id = 47720)

print recurring


# recurring = pybillomat.Recurring.create(
#     conn = conn,
#     client_id = 447505,
#     name = u"TEST NAME 7",
#     payment_types = u"BANK_TRANSFER",
#     next_creation_date = u"",
#     template_id = 29207
# )
#
# print recurring

recurring_item = pybillomat.RecurringItem(conn = conn)
