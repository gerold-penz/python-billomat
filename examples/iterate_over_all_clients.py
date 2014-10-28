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

# This example iterates over ALL clients. It loads the clients gradually. In
# pages of 30 clients.

clients = pybillomat.ClientsIterator(conn = conn, per_page = 30)
clients.search()

for client in clients:
    assert isinstance(client, pybillomat.Client)
    print client.name

print len(clients)
