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


# Iterate over the properties of one client.
# It loads the properties gradually. In pages of 100 properties.
clients_properties_iterator = pybillomat.ClientsPropertiesIterator(conn = conn)
clients_properties_iterator.search(client_id = 81257)
for clients_property in clients_properties_iterator:
    assert isinstance(clients_property, pybillomat.ClientsProperty)
    print clients_property

