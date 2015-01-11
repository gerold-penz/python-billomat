#!/usr/bin/env python
# coding: utf-8

import pybillomat


# HTTP-Connection to Billomat
conn = pybillomat.Connection(
    billomat_id = "<BillomatId>",
    billomat_api_key = "<BillomatApiKey",
)


# Load one clients-property
clients_property = pybillomat.ClientProperty(conn = conn, id = 123)
print clients_property
# --> ClientsProperty(id=123, ..., name=u'Test', type=u'TEXTFIELD', value=u'Test')


# This example iterates over ALL properties. It loads the properties gradually.
# In pages of 100 properties.
clients_properties_iterator = pybillomat.ClientPropertiesIterator(conn = conn)
clients_properties_iterator.search()
for clients_property in clients_properties_iterator:
    assert isinstance(clients_property, pybillomat.ClientProperty)
    print clients_property


# Iterate over the first 200 properties
clients_properties_iterator = pybillomat.ClientPropertiesIterator(
    conn = conn, per_page = 100
)
clients_properties_iterator.search()
for clients_property in clients_properties_iterator[:200]:
    assert isinstance(clients_property, pybillomat.ClientProperty)
    print clients_property


# Iterate over the properties with the given *client_property_id*.
# It loads the properties gradually. In pages of 100 properties.
clients_properties_iterator = pybillomat.ClientPropertiesIterator(conn = conn)
clients_properties_iterator.search(client_property_id = 2017)
for clients_property in clients_properties_iterator:
    assert isinstance(clients_property, pybillomat.ClientProperty)
    print clients_property


# Iterate over the properties of one client.
# It loads the properties gradually. In pages of 100 properties.
clients_properties_iterator = pybillomat.ClientPropertiesIterator(conn = conn)
clients_properties_iterator.search(client_id = 81257)
for clients_property in clients_properties_iterator:
    assert isinstance(clients_property, pybillomat.ClientProperty)
    print clients_property
