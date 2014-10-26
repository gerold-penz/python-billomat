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
    billomat_id = "immoads",
    billomat_api_key = "87dc4d9db0ef92365b241701262c2415",
    billomat_app_id = 70,
    billomat_app_secret = "4bb31d33c91c4977555e35c84680f7c9"
)

client = pybillomat.Client.get(conn, id = "myself")

print client
print client.id
print client["id"]
