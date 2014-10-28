#!/usr/bin/env python
# coding: utf-8

import pybillomat


# HTTP-Connection to Billomat
conn = pybillomat.Connection(
    billomat_id = "<BillomatId>",
    billomat_api_key = "<BillomatApiKey",
)


# Load one client
client = pybillomat.Client(conn = conn)
client.load(id = 422909)
print client
# --> Client(id=422909, name=u'TESTFIRMA', ...)


# Load all clients into memory
# WARNING! This example loads ALL (really ALL) clients into memory
clients = pybillomat.Clients(conn = conn)
clients.search(fetch_all = True, allow_empty_filter = True)
for client in clients:
    assert isinstance(client, pybillomat.Client)
    print client.name


# This example iterates over ALL clients. It loads the clients gradually. In
# pages of 30 clients.
clients_iterator = pybillomat.ClientsIterator(conn = conn, per_page = 30)
clients_iterator.search()
for client in clients_iterator:
    assert isinstance(client, pybillomat.Client)
    print client.name


# Iterate over the first 10 clients (5 per page)
clients_iterator = pybillomat.ClientsIterator(conn = conn, per_page = 5)
clients_iterator.search()
for client in clients_iterator[:10]:
    assert isinstance(client, pybillomat.Client)
    print client.name


