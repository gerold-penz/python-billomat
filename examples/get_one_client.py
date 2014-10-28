#!/usr/bin/env python
# coding: utf-8

# BEGIN --- required only for testing, remove in real world code --- BEGIN
import os
import sys
THISDIR = os.path.dirname(os.path.abspath(__file__))
APPDIR = os.path.abspath(os.path.join(THISDIR, os.path.pardir))
sys.path.insert(0, APPDIR)
# END --- required only for testing, remove in real world code --- END


import pybillomat

conn = pybillomat.Connection(
    billomat_id = "<BillomatId>",
    billomat_api_key = "<BillomatApiKey",
)

client = pybillomat.Client(conn = conn)
client.load(id = 422909)
print client
# --> Client(
#     id=422909,
#     client_number=u'K10141005',
#     created=datetime.datetime(2014, 10, 27, 11, 24, 49),
#     name=u'TESTFIRMA',
#     first_name=u'TESTVORNAME',
#     last_name=u'TESTNACHNAME',
#     ...
# )

