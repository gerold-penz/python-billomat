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


client_properties_iterator = pybillomat.ClientPropertiesIterator(conn = conn)
client_properties_iterator.per_page = 3
client_properties_iterator.search(
    client_property_id = 3408,  # Immoads Kundennummer
    value = u"238701"
)

for index, client_property in enumerate(client_properties_iterator):
    print repr(client_property)
    if index == 2:
        break
